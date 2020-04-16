from django.shortcuts import render,  get_object_or_404

from .models import Entity, Entity_type, History

import datetime


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
            type_name = type_list[0].name
        ent_type = Entity_type.objects.get(name=type_name)
    except Entity_type.DoesNotExist:
        del request.COOKIES["chosen_type"]
        ent_type = Entity_type.objects.get(name=type_list[0].name)
    # Entity
    try:
        serial_num_list = Entity.objects.all().filter(entity_name=ent_type)
        if "chosen_serial_num" in request.COOKIES:
            serial_number = request.COOKIES["chosen_serial_num"]
        else:
            serial_number = serial_num_list[0].serial_num
        ent = Entity.objects.get(serial_num=serial_number)
    except Entity.DoesNotExist:
        del request.COOKIES["chosen_serial_num"]
        ent = Entity.objects.get(serial_num=serial_num_list[0].serial_num)
    # History
    # try:    
    #     history_sample = History.objects.all().filter(serial_num=ent).order_by('date_taken')       
    # except History.DoesNotExist:
    #     history_sample = None
    # if history_sample:
    #     if ent.status:
    #         date_taken = datetime.date()
    #         date_return = 'YYYY-MM-DD'
    #         user_taken = None 
    #         user_return = None 
    #         admin_taken = None #Имя залогиненного админа
    #         admin_return = None
    #     else:
    #         date_taken = history_sample.date_taken
    #         date_return = datetime.date()
    #         user_taken = format_name(history_sample.user_taken) #Имя пользователя 
    #         user_return = None
    #         admin_taken = format_name(history_sample.admin_taken)
    #         admin_return = 'Имя залогиненного админа' #Имя залогиненного админа

    #     hist = {
    #         "number": history_sample.id,
    #         "place": history_sample.place,
    #         "comment": history_sample.comment,
    #         "date": {
    #             "taken":date_taken,
    #             "return":date_return,
    #         }
    #         "user": {
    #             "taken":user_taken,
    #             "return":user_return,
    #         }
    #         "admin": {
    #             "taken":admin_taken,
    #             "return":admin_return,
    #         },

    #     }
    # else:
    #     hist = {
    #         "number": history_sample.id,
    #         "place": history_sample.place,
    #         "comment": history_sample.comment,
    #         "date": {
    #             "taken":date_taken,
    #             "return":date_return,
    #         }
    #         "user": {
    #             "taken":user_taken,
    #             "return":user_return,
    #         }
    #         "admin": {
    #             "taken":admin_taken,
    #             "return":admin_return,
    #         },

    #     }

    context = {
                'chosen_type': ent_type,
                'type_list': type_list,                                      
                'chosen_entity': ent,
                'serial_num_list': serial_num_list,   
                # 'history_sample':history_sample,                                          
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