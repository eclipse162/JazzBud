from django.urls import path
from .views import AuthURL, auth_callback, IsAuthenticated

app_name = 'core'

urlpatterns = [
    path('auth', AuthURL.as_view(), name='auth'),
    path('redirect', auth_callback, name='redirect'),
    path('is-authenticated', IsAuthenticated.as_view(), name='is-authenticated')
]