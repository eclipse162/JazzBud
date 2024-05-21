from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import *
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('auth-url', views.SpotifyRequestUserAuth.as_view(), name='auth-url'),
    path('redirect', views.spotify_redirect, name='redirect'),
    path('check-auth', views.ConfirmAuth.as_view(), name='check-auth'),
    path('current-song', views.CurrentSong.as_view(), name='current-song'),
]