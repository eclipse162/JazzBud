from django.urls import path
from .views import AuthURL, auth_callback, IsAuthenticated, SpotifyAPI

app_name = 'core'

urlpatterns = [
    path('auth', AuthURL.as_view(), name='auth'),
    path('redirect', auth_callback, name='redirect'),
    path('user_info', SpotifyAPI.as_view(), name='user_info'),
    path('is-authenticated', IsAuthenticated.as_view(), name='is-authenticated')
]