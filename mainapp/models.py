import os
from DBU import settings
from django.db import models
from django.contrib.auth.models import User

def images_path():
    return os.path.join(settings.MEDIA_ROOT, 'images')

def label_path():
    return os.path.join(settings.BASE_DIR, 'documents/labels')

class Entity_type(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    img_link = models.ImageField(upload_to='images/')
    soft_link = models.CharField(max_length=200)
    additional_info = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Entity(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, default=1)   
    serial_num = models.CharField(max_length=200)
    entity_name = models.ForeignKey(Entity_type, on_delete=models.CASCADE)
    status = models.BooleanField()
    spec_check = models.BooleanField()
    date_made = models.DateField(null=True)
    date_delivered = models.DateField(null=True)
    doc_delivered = models.CharField(max_length=200)
    label = models.FilePathField(path=label_path)
    label_original = models.CharField(max_length=200)
    note = models.CharField(max_length=400) 

class History(models.Model):    
    id =  models.AutoField(auto_created=True, primary_key=True, default=1, unique=True)  
    serial_num = models.CharField(max_length=200)
    date_taken = models.DateField(null=True)
    date_return = models.DateField(null=True)
    user_taken = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+')
    admin_taken = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+')
    admin_return = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+', null=True)
    place = models.CharField(max_length=200)
    comment = models.CharField(max_length=400, null=True, blank=True)