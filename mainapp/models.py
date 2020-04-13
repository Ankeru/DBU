import os
from DBU import settings
# from django.db import models
# from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def images_path():
    return os.path.join(settings.BASE_DIR, 'img')

def label_path():
    return os.path.join(settings.BASE_DIR, 'documents/labels')

class Entity_type(models.Model):
    name = models.CharField(max_length=200)
    img_link = models.FilePathField(path=images_path)
    soft_link = models.CharField(max_length=200)
    additional_info = models.CharField(max_length=200)

class Entity(models.Model):    
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
    serial_num =  models.ForeignKey(Entity, on_delete=models.CASCADE)
    date_taken = models.DateField()
    date_return = models.DateField()
    user_taken = models.ForeignKey(User)
    admin_taken = models.ForeignKey(User)
    admin_return = models.ForeignKey(User)
    place = models.CharField(max_length=200)
    comment = models.CharField(max_length=400)
