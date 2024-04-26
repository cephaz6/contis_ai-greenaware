from django.shortcuts import render, redirect
from app.controllers.authentication import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def home(request):
    return render(request, 'index.html')



@csrf_exempt
def register(request):
    if request.method == 'POST':
        print(request)
        return register_user(request)
    else:
        return render(request, 'authentication/register.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        print(request)
        return login_user(request)
    else:
        return render(request, 'authentication/login.html')
