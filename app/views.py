from django.shortcuts import render, redirect


def home(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'authentication/login.html')