from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
<<<<<<< HEAD
    path('', views.index, name='index')
]
=======
    path('', views.index, name='index'),
    path('about/', views.about, name='about')
]
>>>>>>> 7ec99a924d38d7f0751dafb726fd549450065a8d
