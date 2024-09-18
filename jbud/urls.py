from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

from core.views import home, login, about, search
urlpatterns = [
    path('', login, name='login'),
    path('about/', about, name='about'),
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('spotify/', include('spotify.urls')),
    path('search/', search, name='search')
]
