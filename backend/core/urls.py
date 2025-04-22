from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    home,
    about,
    login,
    search,
    artist,
    album,
    track,
    artist_search,
    instrument_search,
    save_artist_selection,
    transfer_playback,
    playback,
)



urlpatterns = [
    path('', login.as_view(), name="login"),
    path('home/', home.as_view(), name="home"),
    path('about/', about.as_view(), name="about"),
    path('search/', search.as_view(), name='search'),

    # Music Pages
    path('track/', track.as_view(), name='track'),
    path('album/', album.as_view(), name='album'),
    path('artist/', artist.as_view(), name='artist'),

    path('artist_search/', artist_search.as_view(), name='artist_search'),
    path('instrument_search/', instrument_search.as_view(), name='instrument_search'),
    path('save_artist_selection/', save_artist_selection, name='save_artist_selection'),
    
    path("transfer-playback/<str:device_id>/", transfer_playback, name="transfer_playback"),
    path("play/<str:track_uri>/<str:action>/", playback, name="play_song"),
]
