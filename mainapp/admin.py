from django.contrib import admin

from .models import Entity, Entity_type, History

admin.site.register(Entity)
admin.site.register(Entity_type)
admin.site.register(History)