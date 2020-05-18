import os
from DBU import settings
from django.db import models
from django.contrib.auth.models import User

def images_path():
    return os.path.join(settings.MEDIA_ROOT, 'images/')

def label_path():
    return os.path.join(settings.MEDIA_ROOT, 'labels/')

def doc_path():
    return os.path.join(settings.MEDIA_ROOT, 'doc/')

class Entity_type(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    img_link = models.ImageField(upload_to='images/', blank=True)
    soft_link = models.CharField(max_length=200, blank=True)
    additional_info = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.name

class Entity(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)   
    serial_num = models.CharField(max_length=200)
    entity_name = models.ForeignKey(Entity_type, on_delete=models.CASCADE)
    status = models.BooleanField()
    spec_check = models.BooleanField()
    date_made = models.DateField(null=True, blank=True)
    date_delivered = models.DateField(null=True, blank=True)
    doc_delivered = models.FilePathField(path=doc_path(), blank=True)
    doc_delivered_original = models.CharField(max_length=200, blank=True)
    label = models.FilePathField(path=label_path(), blank=True)
    label_original = models.CharField(max_length=200, blank=True)
    note = models.CharField(max_length=400, blank=True) 

class History(models.Model):    
    record_num =  models.BigIntegerField(blank=False)  
    serial_num = models.ForeignKey(Entity, on_delete=models.CASCADE)
    date_taken = models.DateField(null=True, blank=True)
    date_return = models.DateField(null=True, blank=True)
    user_taken = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+', blank=True)
    admin_taken = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+', blank=True)
    admin_return = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+', null=True, blank=True)
    place = models.CharField(max_length=200, blank=True)
    comment = models.CharField(max_length=400, null=True, blank=True)