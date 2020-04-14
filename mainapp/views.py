from django.shortcuts import render,  get_object_or_404

from .models import Entity, Entity_type, History


def index(request, type_name, serial_number):
    # Entity_type
    type_list = Entity_type.name
    ent_type = get_object_or_404(Entity_type.objects, name=type_name)
    # Entity
    serial_num_list = Entity.entity_name
    ent = get_object_or_404(Entity.objects, serial_num=serial_number)
    context = {
                'chosen_type': ent_type,
                'type_list': type_list,                                      
                'chosen_entity': ent,
                'serial_num_list': serial_num_list,                             
                }
    # context = {}
    return render(request, 'mainapp/index.html', context)