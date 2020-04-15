from django.shortcuts import render,  get_object_or_404

from .models import Entity, Entity_type, History

def index(request):
    # Entity_type
    type_list = Entity_type.objects.all()
    if "chosen_type" in request.session:
        type_name = request.session["chosen_type"]
    else:
        type_name = type_list[0].name
    ent_type = get_object_or_404(Entity_type.objects, name=type_name)
    # Entity
    serial_num_list = Entity.objects.all().filter(entity_name=ent_type)
    if "chosen_serial_num" in request.session:
        serial_number = request.session["chosen_serial_num"]
    else:
        serial_number = serial_num_list[0].name
    ent = get_object_or_404(Entity.objects, serial_num=serial_number)
    context = {
                'chosen_type': ent_type,
                'type_list': type_list,                                      
                'chosen_entity': ent,
                'serial_num_list': serial_num_list,   
                'request': request,                          
                }
    # context = {}
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