from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

from core.views import home, login, about, search, artist, album, track, artist_search, instrument_search, save_artist_selection, transfer_playback, playback
urlpatterns = [
    path('', login.as_view(), name="login"),
    path("home/", home.as_view(), name="home"),
    path("about/", about.as_view(), name="about"),
    path('search/', search.as_view(), name='search'),

    # Music Pages
    path('track/', track.as_view(), name='track'),
    path('album/', album.as_view(), name='album'),
    path('artist/', artist.as_view(), name='artist'),
    
    path('admin/', admin.site.urls),
    path('about/', include('core.urls')),
    path('spotify/', include('spotify.urls')),
]
