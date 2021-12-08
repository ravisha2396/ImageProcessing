from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('capture', views.capture, name='capture'),
    path('remove', views.remove, name='remove')

]