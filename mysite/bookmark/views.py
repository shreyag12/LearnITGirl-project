# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from login.forms import *
from bookmark.forms import signUpForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
# Create your views here.

def index(request):
        return render(
        request,
        'index.html',
    )
def register(request):
    if request.method == 'POST':
        form = signUpForm(request.POST) # Create a form instance and populate it with data from the request (binding):
        if form.is_valid():
            user=User.objects.create_user(
            email=form.cleaned_data['email'],
            password = form.cleaned_data['Password'],
            password2 = form.cleaned_data['Confirm password']
            )
            return HttpResponseRedirect('/register/success/')
# If this is a GET (or any other method) create the default form.
    else:
        form = signUpForm()
    return render(request, 'register.html', {'form': form})
def login(request):
    return render(
    request,
    'login.html',
    )
def register_success(request):
    return render(
        request,
        'success.html',
        )

