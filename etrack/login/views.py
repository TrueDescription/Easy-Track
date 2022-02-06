from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login as l
from django.contrib.auth import authenticate, logout


# Create your views here.

def login(response):
    if response.method == "POST":
        username = response.POST.get('username')
        password = response.POST.get('password')
        user = authenticate(response, username=username, password=password)
        if user is not None:
            l(response, user)
            return redirect('http://127.0.0.1:8000/')
        else:
            messages.info(response, 'Username or password is incorrect')
    return render(response, 'login/loginpage.html', {})


def logoutUser(response):
    logout(response)
    return redirect('login')
