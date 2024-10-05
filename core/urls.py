from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('<str:artist_name>/', views.artist_page, name='artist_page'),
    path('<str:artist_name>/<str:album_title>/', views.album_page, name='album_page')
]
