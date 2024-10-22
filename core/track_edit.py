import re, os
import spotipy
import requests
from core.views import search
from db.database import get_db
from requests import request, get
from spotify.views import refresh_user
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
ARTIST_STORAGE = []
ROWS = []
