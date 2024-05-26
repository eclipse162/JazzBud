from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import *
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about')
]
