from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login,logout
from django import forms
from backend.forms import UserRegistrationForm,UserLoginForm
from django.db.models import Q
from django.conf import settings
from backend.models import *
from frontend.models import *
import json
from backend.decorators import (
   permission_required,
   xhr_request_only,
   # add_edit_permission
)

def index(request):
    return render(request,"index.html")
    
def login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
       
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('dashboard')
        else:
            # messages.info(request, f'account done not exit plz sign in')
            messages.error(request,'username or password not correct')
    form = UserLoginForm()
    return render(request, 'login.html', {'form':form, 'title':'log in'})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
       
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
               #  print(password)
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return redirect('login')
                # return HttpResponseRedirect('/')    
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
                
    else:
        form = UserRegistrationForm()
        
    return render(request, 'register.html', {'form' : form})

def logout(request):
   request.session.flush()  
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))








  
