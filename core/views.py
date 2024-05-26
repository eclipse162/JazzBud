import os
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'core/index.html')
    
def about(request):
    return render(request, 'core/about.html')
