from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),

    path('<str:artist_name>/<str:artist_id>', views.artist_page, name='artist_page'),
    path('album/<str:artist_name>/<str:album_title>/<str:album_id>', views.album_page, name='album_page'),
    path('track/<str:artist_name>/<str:track_title>/<str:track_id>', views.track_page, name='track_page'),

    path('artist_search/', views.artist_search, name='artist_search'),
    path('instrument_search/', views.instrument_search, name='instrument_search'),
    path('save_artist_selection/', views.save_artist_selection, name='save_artist_selection'),
    
    path("transfer-playback/<str:device_id>/", views.transfer_playback, name="transfer_playback"),
    path("play/<str:track_uri>/<str:action>/", views.playback, name="play_song"),

]
