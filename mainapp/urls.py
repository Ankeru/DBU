from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('proccess_index_form/', views.proccess_index_form, name='proccess_index_form'),
    path('view/', views.view, name='view'),
    path('<str:type_>/view_type/', views.view_type, name='view_type'),
    path('<str:type_>/<str:serial_num>/view_serial_num/', views.view_serial_num, name='view_serial_num'),
    path('proccess_type_form/', views.proccess_type_form, name='proccess_type_form'),
    path('proccess_profile_form/', views.proccess_profile_form, name='proccess_profile_form'),

]
if settings.DEBUG:
    # urlpatterns += [
    #     url(r'^media/(?P<path>.*)$', serve,
    #     {'document_root': settings.MEDIA_ROOT}),
    # ]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
