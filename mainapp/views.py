import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Entity, Entity_type, History
from django.conf import settings
from django.conf.urls.static import static

import os
from DBU.settings import MEDIA_ROOT, MEDIA_URL


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
                    serial_num=ent.serial_num,
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


def proccess_type_form(request):
    type_ = request.POST["type_"]
    add_info = request.POST["additional_info"]
    my_file = request.FILES['img_file']
    #Меняем путь до картинки
    change_img_path = Entity_type.objects.get(name=type_)
    change_img_path.img_link = my_file.name
    change_img_path.save()
    #Загружаем картитнку
    handle_uploaded_file(my_file, my_file.name)
    return HttpResponseRedirect(reverse( "view_type", args=(type_, )))


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
            history_sample = History.objects.all().filter(serial_num=ent.serial_num).order_by('date_taken')  
            if (request.user.is_authenticated and request.user.is_staff) :                
                should_fill = True
                if ((len(history_sample) > 0 ) and (not ent.status)):
                    history_sample = history_sample[0]
                    date_taken = str(history_sample.date_taken.year) + '-' + str(history_sample.date_taken.month).rjust(2, '0') + '-' + str(history_sample.date_taken.day).rjust(2, '0')               
                    date_return = str(datetime.date.today().year) + '-' + str(datetime.date.today().month).rjust(2, '0') + '-' + str(datetime.date.today().day).rjust(2, '0')
                    user_taken = history_sample.user_taken.username
                    admin_taken = history_sample.admin_taken.username
                    admin_return = request.user.username                    
                    comment = history_sample.comment
                    number = History.objects.all().count()
                    place = history_sample.place
                else:
                    date_taken = str(datetime.date.today().year) + '-' + str(datetime.date.today().month).rjust(2, '0') + '-' + str(datetime.date.today().day).rjust(2, '0')
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
                    date_taken =  str(history_sample.date_taken.year) + '-' + str(history_sample.date_taken.month).rjust(2, '0') + '-' + str(history_sample.date_taken.day).rjust(2, '0')               
                    date_return = str(history_sample.date_return.year) + '-' + str(history_sample.date_return.month).rjust(2, '0') + '-' + str(history_sample.date_return.day).rjust(2, '0')               
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

def view(request):
    # Entity_type
    Entity_list = Entity.objects.all()
    # ent_type = get_object_or_404(Entity_type.objects, name=type_name)
    # request.session["chosen_type"] = type_name
    # Entity
    # serial_num_list = Entity.objects.all()
    # ent = get_object_or_404(Entity.objects, serial_num=serial_number)
    # request.session["chosen_serial_num"] = serial_number
    
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
        "type_sample": type_sample
    }
    return render(request, 'mainapp/view_type.html', context)

def view_serial_num(request, type_, serial_num):
    Entity_ = Entity.objects.all().get(entity_name=Entity_type.objects.all().get(name=type_), serial_num=serial_num)    
    context = {
        "Entity": Entity_,
        "type": type_,
        "serial_num": serial_num,
    }
    return render(request, 'mainapp/view_serial_num.html', context)
