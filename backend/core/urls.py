from . import views

from django.urls import path
from views import home, about, login, search
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', login.as_view(), name="login"),
    path('home/', home.as_view(), name="home"),
    path('about/', about.as_view(), name="about"),
    path('search/', search.as_view(), name='search'),

    path('<str:artist_name>/<str:artist_id>', views.artist, name='artist_page'),
    path('album/<str:artist_name>/<str:album_title>/<str:album_id>', views.album, name='album_page'),
    path('track/<str:artist_name>/<str:track_title>/<str:track_id>', views.track, name='track_page'),

    path('artist_search/', views.artist_search, name='artist_search'),
    path('instrument_search/', views.instrument_search, name='instrument_search'),
    path('save_artist_selection/', views.save_artist_selection, name='save_artist_selection'),
    
    path("transfer-playback/<str:device_id>/", views.transfer_playback, name="transfer_playback"),
    path("play/<str:track_uri>/<str:action>/", views.playback, name="play_song"),

]
