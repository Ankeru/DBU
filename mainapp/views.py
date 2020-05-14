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
                his = History.objects.get(id=request.POST['number'])
                his.date_return=request.POST['date_return']
                his.admin_return=User.objects.get(username=request.POST['admin_return'])
                his.comment=request.POST['comment']
                his.save()
                ent.status = True
                ent.save()
            else:
                his = History(   
                    id = History.objects.all().count()+1,             
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
            relative_path = os.path.join("labels", doc_delivered_file.name)
            entity_sample.doc_delivered = os.path.join(MEDIA_URL, relative_path)             
            #Загружаем файл
            handle_uploaded_file(doc_delivered_file, relative_path)    
        label_ref_file = request.FILES.get('label_ref')
        if label_ref_file is not None:
            relative_path = os.path.join("labels",label_ref_file.name) 
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
        relative_path = os.path.join("images",my_file.name)
        #Меняем путь до картинки        
        change_type_sample.img_link = os.path.join(MEDIA_URL, relative_path)             
        #Загружаем картитнку
        handle_uploaded_file(my_file, relative_path)    
    change_type_sample.soft_link = request.POST["loc_of_soft"]
    change_type_sample.additional_info = request.POST["additional_info"]
    change_type_sample.save()

    return HttpResponseRedirect(reverse( "view_type", args=(type_, )))
# Обработчик формы изменения истории
def proccess_history_form(request):
    type_ = request.POST["hidden_type"]
    serial_num = request.POST["hidden_serial_num"]
    id_num = request.POST["seans_number"]
    history_sample = History.objects.get(id=id_num,
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
            history_sample = History.objects.all().filter(serial_num=ent).order_by('date_taken')  
            if (request.user.is_authenticated and request.user.is_staff) :                
                should_fill = True
                if ((len(history_sample) > 0 ) and (not ent.status)):
                    history_sample = history_sample[0]
                    date_taken = history_sample.date_taken
                    date_return = datetime.date.today()
                    user_taken = history_sample.user_taken.username
                    admin_taken = history_sample.admin_taken.username
                    admin_return = request.user.username                    
                    comment = history_sample.comment
                    number = History.objects.all().count()
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
                        number= History.objects.all().count() + 1
                    else:
                        number = "1"
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
                    number= History.objects.all().count()
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
                "number": "1",
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
                }
    return render(request, 'mainapp/index.html', context)

def edit(request):
    type_list = Entity_type.objects.all()
    context = {
        "type_list": type_list, 
    }
    return render(request, 'mainapp/edit.html', context)

def view(request):
    Entity_list = Entity.objects.all()    
    context = {"Entity_list": Entity_list}
    return render(request, 'mainapp/view.html', context)

def view_type(request, type_):
    type_list = Entity_type.objects.all()
    Entity_list = Entity.objects.all().filter(entity_name=Entity_type.objects.all().get(name=type_)) 
    type_sample = type_list.get(name=type_)
    context = {
        "Entity_list": Entity_list,
        "type": type_,
        "type_list": type_list, 
        "type_sample": type_sample,
    }
    return render(request, 'mainapp/view_type.html', context)

def view_serial_num(request, type_, serial_num):
    type_list = Entity_type.objects.all()
    entity_list = Entity.objects.all()
    entity_ = entity_list.get(entity_name=Entity_type.objects.all().get(name=type_), serial_num=serial_num)    
    type_sample = type_list.get(name=type_) 
    history_list = History.objects.order_by("-id")
    context = {
        "type": type_,
        "type_sample": type_sample,
        "type_list": type_list,
        "Entity": entity_,
        "entity_list": entity_list,        
        "serial_num": serial_num,
        "history_list": history_list,
        "users_list": User.objects.all(),
    }
    return render(request, 'mainapp/view_serial_num.html', context)
