import os
from DBU import settings
from django.db import models
from django.contrib.auth.models import User

def images_path():
    return os.path.join(settings.BASE_DIR, 'img')

def label_path():
    return os.path.join(settings.BASE_DIR, 'documents/labels')

class Entity_type(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    img_link = models.FilePathField(path=images_path)
    soft_link = models.CharField(max_length=200)
    additional_info = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Entity(models.Model):    
    serial_num = models.CharField(max_length=200, primary_key=True)
    entity_name = models.ForeignKey(Entity_type, on_delete=models.CASCADE)
    status = models.BooleanField()
    spec_check = models.BooleanField()
    date_made = models.DateField()
    date_delivered = models.DateField()
    doc_delivered = models.CharField(max_length=200)
    label = models.FilePathField(path=label_path)
    label_original = models.CharField(max_length=200)
    note = models.CharField(max_length=400) 
    
    def __str__(self):
        return self.serial_num

class History(models.Model):    
    serial_num =  models.ForeignKey(Entity, on_delete=models.CASCADE)
    date_taken = models.DateField()
    date_return = models.DateField()
    user_taken = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+')
    admin_taken = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+')
    admin_return = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+')
    place = models.CharField(max_length=200)
    comment = models.CharField(max_length=400)


    # e = Entity(entity_name=Entity_type.objects.all()[0].name, status='True', spec_check='True', date_made="2020-12-12", date_delivered="2020-12-12", doc_delivered='pifpaf', label='aaa', label_original='in_bathroom', note='sdf')
# Entity_type(name="1", img_link="2", soft_link='3', additional_info="1")
# with open(f'/home/ankeru/Рабочий стол/Проекты/DBU/log.txt', 'a') as f:
            #     f.write(' type_name=True')