from django.urls import path, include


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('proccess_index_form/', views.proccess_index_form, name='proccess_index_form'),
    path('view/', views.view, name='view'),
    path('<str:type_>/view_type/', views.view_type, name='view_type'),
    path('<str:type_>/<str:serial_num>/view_serial_num/', views.view_serial_num, name='view_serial_num'),
]
