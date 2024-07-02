from django.shortcuts import render

def login(request):
    return render(request, 'core/login.html')

def about(request):
    return render(request, 'core/about.html')

def home(request):
    return render(request, 'core/index.html')
