from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login_redirect/', views.login_redirect, name='login_redirect'),
    path('proccess_index_form/', views.proccess_index_form, name='proccess_index_form'),
    path('view/', views.view, name='view'),
    path('<str:type_>/view_type/', views.view_type, name='view_type'),
    path('<str:type_>/<str:serial_num>/view_serial_num/', views.view_serial_num, name='view_serial_num'),
    path('edit/', views.edit, name='edit'),
    path('proccess_type_form/', views.proccess_type_form, name='proccess_type_form'),
    path('<str:type_>/proccess_profile_form/', views.proccess_profile_form, name='proccess_profile_form'),
    path('proccess_history_form/', views.proccess_history_form, name='proccess_history_form'),
    path('proccess_edit_form/', views.proccess_edit_form, name='proccess_edit_form'),
    path('<str:uname>/profiles/', views.profiles, name='profiles'),
    path('<int:added>/edit_complete/', views.edit_complete, name='edit_complete'),
    path('types/', views.types, name='types'),
    
]
