import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Entity, Entity_type, History
from django.conf import settings
from django.conf.urls.static import static

import os
from DBU.settings import MEDIA_ROOT, MEDIA_URL, STATIC_URL
import sys

MAX_FILE_SIZE = 1*1024*1024
MAX_PHOTO_SIZE = 1*1024*1024
# Обработчик кнопки "Принять"/"Выдать"
def proccess_index_form(request):
    try:
        ent_type = Entity_type.objects.get(name=request.POST.get('type', default="notexist"))
    except Entity_type.DoesNotExist:
        ent_type = None

    if ent_type:
        try:
            ent = Entity.objects.get(
                                    serial_num=request.POST.get('serial_num', default="notexist"),
                                    entity_name=ent_type
                                    )
        except Entity.DoesNotExist:
            ent = None  
        if ent is not None:
            if request.POST['free'] == "0":
                his = History.objects.get(record_num=int(request.POST['number']), serial_num=Entity.objects.all().get(serial_num=request.POST.get('serial_num', default="notexist"), entity_name=Entity_type.objects.get(name=request.POST.get('type', default="notexist"))) )
                his.date_return=request.POST['date_return']
                his.admin_return=User.objects.get(username=request.POST['admin_return'])
                his.comment=request.POST['comment']
                his.save()
                ent.status = True
                ent.save()
            else:
                his = History(   
                    record_num = History.objects.all().filter(serial_num=ent).count()+1,             
                    serial_num=ent,
                    date_taken=request.POST['date_taken'],            
                    user_taken=User.objects.get(username=request.POST['user_taken']),
                    admin_taken=User.objects.get(username=request.POST['admin_taken']),
                    place=request.POST['location'],
                    comment=request.POST['comment'],
                                 )
                his.save()
                ent.status = False
                ent.save()

    return HttpResponseRedirect(reverse('index', args=()))

# Обработчик кнопки "Сохранить изменения в Анкете"
def proccess_profile_form(request):
    if "chosen_type" in request.COOKIES: 
        # Работа с не-файловыми полями
        type_ = request.COOKIES["chosen_type"]
        serial_num = request.POST["serial_num"]
        entity_sample = Entity.objects.get(entity_name=Entity_type.objects.get(name=type_),
                                        serial_num=serial_num)
        entity_sample.status = ("available" in request.POST)
        entity_sample.spec_check = ("special_check" in request.POST)  
        if request.POST['production_date']:
            entity_sample.date_made = request.POST['production_date']
        if request.POST['date_of_delivery']:
            entity_sample.date_delivered = request.POST['date_of_delivery']    
               
        entity_sample.doc_delivered_original  = request.POST['loc_of_storage_original_delivery_document']
        entity_sample.label_original = request.POST['loc_of_storage_original_label']
        entity_sample.note = request.POST['note']
        # Работа с файлами
        doc_delivered_file = request.FILES.get('delivery_document')
        if doc_delivered_file is not None:
            if doc_delivered_file.size <= MAX_FILE_SIZE:
                relative_path = os.path.join("doc", serial_num + "_doc." + doc_delivered_file.name.split('.')[-1])
                entity_sample.doc_delivered = os.path.join(MEDIA_URL, relative_path)             
                #Загружаем файл
                handle_uploaded_file(doc_delivered_file, relative_path)    
        label_ref_file = request.FILES.get('label_ref')
        if label_ref_file is not None:
            if label_ref_file.size <= MAX_FILE_SIZE:
                relative_path = os.path.join("labels", serial_num + "_label." + label_ref_file.name.split('.')[-1]) 
                entity_sample.label = os.path.join(MEDIA_URL, relative_path)                
                #Загружаем файл
                handle_uploaded_file(label_ref_file, relative_path)    
        # Сохранение изменений
        entity_sample.save()
    return HttpResponseRedirect(reverse( "view_serial_num", args=(type_,serial_num, )))

# Обработчик формы изменения типа
def proccess_type_form(request):
    type_ = request.POST["type_"]
    add_info = request.POST["additional_info"]
    my_file = request.FILES.get('img_file')
    change_type_sample = Entity_type.objects.get(name=type_)
    if my_file is not None:
        if my_file.size <= MAX_PHOTO_SIZE:
            # relative_path = os.path.join("images", my_file.name)
            relative_path = os.path.join("images", type_ + "_img." + my_file.name.split('.')[-1])
            #Меняем путь до картинки        
            change_type_sample.img_link = os.path.join(MEDIA_URL, relative_path)             
            #Загружаем картитнку
            handle_uploaded_file(my_file, relative_path)    
    change_type_sample.soft_link = request.POST["loc_of_soft"]
    change_type_sample.additional_info = request.POST["additional_info"]
    if request.POST.get('new_type_name_cb', False):
        new_type_name = request.POST.get('new_type_name', "")
        if new_type_name:
            change_type_sample.name = new_type_name

    change_type_sample.save()

    return HttpResponseRedirect(reverse( "view_type", args=(type_, )))

# Обработчик формы изменения истории
def proccess_history_form(request):
    type_ = request.POST["hidden_type"]
    serial_num = request.POST["hidden_serial_num"]
    id_num = request.POST["seans_number"]
    history_sample = History.objects.get(record_num=int(id_num),
        serial_num=Entity.objects.get(serial_num=serial_num,
         entity_name=Entity_type.objects.get(name=type_)))
    history_sample.date_taken = request.POST["date_taken"]
    history_sample.date_return = request.POST["date_return"]
    history_sample.user_taken = User.objects.get(username=request.POST["user_"])
    history_sample.place = request.POST["place"]
    history_sample.comment = request.POST["comment"]
    history_sample.save()
    return HttpResponseRedirect(reverse( "view_serial_num", args=(type_, serial_num, )))
    
def handle_uploaded_file(f, file_name):
    with open(os.path.join(MEDIA_ROOT, file_name), 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
    
def index(request):
    try:
        if request.user.is_authenticated:
            uname = request.user.username 
        else:
            uname = 'noname'
        # Entity_type
        type_list = Entity_type.objects.all()        
        if "chosen_type" in request.COOKIES:            
            type_name = request.COOKIES["chosen_type"]
        else:
            if len(type_list) > 0:
                type_name = type_list[0].name
            else: 
                type_name = None
        ent_type = Entity_type.objects.get(name=type_name)
    except Entity_type.DoesNotExist:
        if len(type_list) > 0:
            ent_type = Entity_type.objects.get(name=type_list[0].name)
        else: 
            ent_type = None

    # Entity
    try:
        serial_num_list = Entity.objects.all().filter(entity_name=ent_type)
        if "chosen_serial_num" in request.COOKIES:
            serial_number = request.COOKIES["chosen_serial_num"]
        else:
            if len(serial_num_list) > 0:
                serial_number = serial_num_list[0].serial_num
            else:
                serial_number = None
        ent = Entity.objects.get(serial_num=serial_number)
    except Entity.DoesNotExist:
        if len(serial_num_list) > 0:
            ent = Entity.objects.get(serial_num=serial_num_list[0].serial_num)
        else:
            ent = None
    should_fill = False    
    # History
    try:    
        if ent is None:
            history_sample = None
        else:
            history_sample = History.objects.all().filter(serial_num=ent).order_by('-record_num')  
            if (request.user.is_authenticated and request.user.is_staff) :                
                should_fill = True
                # Если сеансы уже были и признак "свободен" выставлен в False
                if ((len(history_sample) > 0 ) and (not ent.status)):
                    history_sample = history_sample[0]
                    date_taken = history_sample.date_taken
                    date_return = datetime.date.today()
                    user_taken = history_sample.user_taken.username
                    admin_taken = history_sample.admin_taken.username
                    admin_return = request.user.username                    
                    comment = history_sample.comment
                    number = History.objects.all().filter(serial_num=ent).count()
                    place = history_sample.place
                else:                   
                    date_taken = datetime.date.today()
                    date_return = 'YYYY-MM-DD'
                    user_taken = User.objects.all() 
                    admin_taken = request.user.username
                    admin_return = ""                    
                    comment = ""
                    place =""
                    if (len(history_sample) > 0 ):                
                        number= History.objects.all().filter(serial_num=ent).count() + 1
                    else:
                        number = 1
            else:
                if (len(history_sample) > 0 ):
                    history_sample = history_sample[0]
                    date_taken = history_sample.date_taken                
                    date_return = history_sample.date_return
                    user_taken = history_sample.user_taken.username
                    admin_taken = history_sample.admin_taken.username
                    admin_return = ""                    
                    comment = history_sample.comment
                    place = history_sample.place
                    number= History.objects.all().filter(serial_num=ent).count()
                    should_fill = True
                else:
                    should_fill = False              
    except History.DoesNotExist:
        history_sample = None
        should_fill = False   
    except IndexError:
        history_sample = None
        should_fill = False        
    if should_fill:
        hist = {                
                "number": number,
                "place": place,
                "comment": comment,
                "date": {
                            "taken":date_taken,
                            "return":date_return,
                        },
                "user": {
                            "taken":user_taken,                    
                        },
                "admin": {
                            "taken":admin_taken,
                            "return":admin_return,
                        },
                }
    else:
        hist = {
                "number": 1,
                "place": "",
                "comment": "",
                "date": {
                            "taken":"YY-MM-DD",
                            "return":"YY-MM-DD",
                        },
                "user": {
                            "taken": "",                    
                        },
                "admin": {
                            "taken":"",
                            "return":"",
                        },
                }        

    context = {
                'chosen_type': ent_type,
                'type_list': type_list,                                      
                'chosen_entity': ent,
                'serial_num_list': serial_num_list,   
                'history_sample':hist, 
                'uname': uname,                                                         
                }
    return render(request, 'mainapp/index.html', context)

def edit(request):
    if request.user.is_authenticated:
        type_list = Entity_type.objects.all()
        if request.user.is_authenticated:
                uname = request.user.username 
        else:
            uname = 'noname'
        context = {
            "type_list": type_list, 
            'uname': uname,
        }
        return render(request, 'mainapp/edit.html', context)
    else:
        context = {}
        # return render(request, 'registration/login.html', context)
        return HttpResponseRedirect(reverse( 'login', args=()))

def view(request):
    Entity_list = Entity.objects.all()
    if request.user.is_authenticated:
            uname = request.user.username 
    else:
        uname = 'noname'    
    context = {
        "Entity_list": Entity_list,
        'uname': uname,
    }
    return render(request, 'mainapp/view.html', context)

def view_type(request, type_):
    type_list = Entity_type.objects.all()
    if request.user.is_authenticated:
            uname = request.user.username 
    else:
        uname = 'noname'
    Entity_list = Entity.objects.all().filter(entity_name=Entity_type.objects.all().get(name=type_)) 
    type_sample = type_list.get(name=type_)
    context = {
        "Entity_list": Entity_list,
        "type": type_,
        "type_list": type_list, 
        "type_sample": type_sample,
        'uname': uname,
    }
    return render(request, 'mainapp/view_type.html', context)

def view_serial_num(request, type_, serial_num):
    type_list = Entity_type.objects.all()
    if request.user.is_authenticated:
            uname = request.user.username 
    else:
        uname = 'noname'
    entity_list = Entity.objects.all()
    entity_ = entity_list.get(entity_name=Entity_type.objects.all().get(name=type_), serial_num=serial_num)    
    type_sample = type_list.get(name=type_) 
    history_list = History.objects.all().filter(serial_num=entity_).order_by("-record_num")
    context = {
        "type": type_,
        "type_sample": type_sample,
        "type_list": type_list,
        "Entity": entity_,
        "entity_list": entity_list,        
        "serial_num": serial_num,
        "history_list": history_list,
        "users_list": User.objects.all(),
        'uname': uname,
    }
    return render(request, 'mainapp/view_serial_num.html', context)

# Обработчик кнопки "Сохранить изменения в Анкете"
def proccess_edit_form(request):
    go_on_with_entityies = False
    if request.POST.get('new_type_cb', False):
        new_type_name = request.POST.get('new_type', "")
        if new_type_name:
            extensible_type = Entity_type(name=new_type_name)
            extensible_type.save()
            go_on_with_entityies = True
    else:
        extensible_type = Entity_type.objects.get(name=request.POST['chosen_type'])
        go_on_with_entityies = True
    if go_on_with_entityies:
        items_edded = 0
        for i in range(1, int(request.POST['hidden_counter'])+1):
            # Проверяем, существует ли объект в словаре
            if request.POST.get('select_serial_num_'+str(i), False):
                # Проверка, нет ли уже такого объекта
                if not Entity.objects.filter(serial_num=request.POST['select_serial_num_'+str(i)], entity_name=extensible_type):                    
                    new_entity = Entity(
                        serial_num=request.POST['select_serial_num_'+str(i)],
                        entity_name=extensible_type,
                        spec_check=request.POST.get('special_check_' + str(i), False),
                        status=True,
                        label_original=request.POST['note_'+str(i)],
                        doc_delivered_original=request.POST['loc_of_storage_original_delivery_document_'+str(i)],
                        )
                    if request.POST.get('production_date_'+str(i), False):
                        new_entity.date_made=request.POST['production_date_'+str(i)]
                    if request.POST.get('date_of_delivery_'+str(i), False):
                        new_entity.date_delivered=request.POST['date_of_delivery_'+str(i)]                        
                    doc_delivered=None,                    
                    label=None,
                    # Работа с файлами
                    doc_delivered_file = request.FILES.get('delivery_document_'+str(i))
                    if doc_delivered_file is not None:
                        relative_path = os.path.join("labels", doc_delivered_file.name)
                        new_entity.doc_delivered = os.path.join(MEDIA_URL, relative_path)             
                        #Загружаем файл
                        handle_uploaded_file(doc_delivered_file, relative_path)    
                    label_ref_file = request.FILES.get('label_ref_'+str(i))
                    if label_ref_file is not None:
                        relative_path = os.path.join("labels",label_ref_file.name) 
                        new_entity.label = os.path.join(MEDIA_URL, relative_path)                
                        #Загружаем файл
                        handle_uploaded_file(label_ref_file, relative_path)                   
                    new_entity.save()
                    items_edded = items_edded + 1
    return HttpResponseRedirect(reverse( "edit_complete", args=(items_edded, )))

def profiles(request, uname):
    if request.user.is_authenticated:
        history_list = History.objects.all().filter(user_taken=User.objects.get(username=uname),
                                                    date_return=None)
        context = {
            'user_list': User.objects.all(),
            'uname': uname,
            'history_list': history_list,
            }
        return render(request, 'mainapp/profiles.html', context)
    else:
        context = {}
        # return render(request, 'registration/login.html', context)
        return HttpResponseRedirect(reverse( 'login', args=()))

def profiles_edit(request):
    if request.user.is_authenticated:
        uname = request.user.username 
    else:
        uname = 'noname'
    context = {
            'uname': uname,            
            }
    return render(request, 'mainapp/profiles_edit.html', context)


def edit_complete(request, added):
    if request.user.is_authenticated:
        uname = request.user.username 
    else:
        uname = 'noname'
    context = {
        "added_num": int(added),
        'uname': uname, 
            }
    return render(request, 'mainapp/edit_complete.html', context)



