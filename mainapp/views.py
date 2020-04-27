import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Entity, Entity_type, History


def proccess_index_form(request):
    if request.POST['free'] == "1":
        return HttpResponseRedirect(reverse('accounts/login', args=()))
    else:
        return HttpResponseRedirect(reverse('index', args=()))

def format_name(with_argunent):
    with with_argunent:
        if (first_name and last_name):
            admin_taken = username + " (" + first_name + " " + last_name + ")" #Имя админа
        else:
            admin_taken = username
    return admin_taken

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
            history_sample = History.objects.all().filter(id=ent.id).order_by('date_taken')       
            if (request.user.is_authenticated()) and (request.user.is_staff) :                
                should_fill = True
                if (history_sample and (not ent.status)):
                    date_taken = history_sample.date_taken
                    date_return = datetime.date()
                    user_taken = history_sample.user_taken.username
                    admin_taken = history_sample.admin_taken.username
                    admin_return = request.user.username                    
                    comment = history_sample.comment
                    number = history_sample.id
                    place = history_sample.place
                else:
                    date_taken = datetime.date()
                    date_return = 'YY-MM-DD'
                    user_taken = User.objects.all() 
                    admin_taken = request.user.username
                    admin_return = ""                    
                    comment = ""
                    if history_sample:
                        number = history_sample.id
                    else:
                        number = "1"
            else:
                if history_sample:
                    date_taken = history_sample.date_taken
                    date_return = history_sample.date_return
                    user_taken = history_sample.user_taken.username
                    admin_taken = history_sample.admin_taken.username
                    admin_return = history_sample.admin_return.username                    
                    comment = history_sample.comment
                    place = history_sample.place
                    should_fill = True
                else:
                    should_fill = False    
            
    except History.DoesNotExist:
        history_sample = None
    
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
                "number": "0",
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

def index_chosen(request, type_name, serial_number):
    # Entity_type
    type_list = Entity_type.objects.all()
    ent_type = get_object_or_404(Entity_type.objects, name=type_name)
    request.session["chosen_type"] = type_name
    # Entity
    serial_num_list = Entity.objects.all()
    ent = get_object_or_404(Entity.objects, serial_num=serial_number)
    request.session["chosen_serial_num"] = serial_number
    context = {
                'chosen_type': ent_type,
                'type_list': type_list,                                      
                'chosen_entity': ent,
                'serial_num_list': serial_num_list,                             
                }
    # context = {}
    return render(request, 'mainapp/index.html', context)
