from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

from core.views import (
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

from spotify.views import (
    AuthURL,
    auth_callback,
    SpotifyAPI,
    IsAuthenticated,
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

    # Spotify API
    path('spotify/auth', AuthURL.as_view(), name='auth'),
    path('spotify/redirect', auth_callback, name='redirect'),
    path('spotify/user_info', SpotifyAPI.as_view(), name='user_info'),
    path('spotify/is-authenticated', IsAuthenticated.as_view(), name='is-authenticated'),

    # Component Helpers
    path('artist-search/', artist_search.as_view(), name='artist-search'),
    path('instrument-search/', instrument_search.as_view(), name='instrument-search'),
    path('save-artist-selection/', save_artist_selection, name='save_artist-selection'),
    
    path("transfer-playback/<str:device_id>/", transfer_playback, name="transfer_playback"),
    path("play/<str:track_uri>/<str:action>/", playback, name="play_song"),
]
