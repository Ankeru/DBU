from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:type_name>/<str:serial_number>/', views.index_chosen, name='index_chosen'),
]