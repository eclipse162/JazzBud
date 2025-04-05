from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

from core.views import home, login, about, search
urlpatterns = [
    path('', login.as_view(), name="login"),
    path("home/", home.as_view(), name="home"),
    path("about/", about.as_view(), name="about"),
    path('search/', search.as_view(), name='search'),
    
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('spotify/', include('spotify.urls')),
]
