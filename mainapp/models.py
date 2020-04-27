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
    id = models.IntegerField(primary_key = True)   
    serial_num = models.CharField(max_length=200)
    entity_name = models.ForeignKey(Entity_type, on_delete=models.CASCADE)
    status = models.BooleanField()
    spec_check = models.BooleanField()
    date_made = models.DateField()
    date_delivered = models.DateField()
    doc_delivered = models.CharField(max_length=200)
    label = models.FilePathField(path=label_path)
    label_original = models.CharField(max_length=200)
    note = models.CharField(max_length=400) 

class History(models.Model):    
    id =  models.ForeignKey(Entity, on_delete=models.CASCADE, primary_key=True, unique=True)
    serial_num = models.CharField(max_length=200)
    date_taken = models.DateField()
    date_return = models.DateField()
    user_taken = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+')
    admin_taken = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+')
    admin_return = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+')
    place = models.CharField(max_length=200)
    comment = models.CharField(max_length=400)