from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('<str:artist_name>/<str:artist_id>', views.artist_page, name='artist_page'),
    path('<str:artist_name>/<str:album_title>/<str:album_id>', views.album_page, name='album_page'),
    path('<str:artist_name>/<str:track_title>/<str:track_id>', views.track_page, name='track_page'),
    path('new_partition/', views.new_partition_page, name='new_partition')
]
