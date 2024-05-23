from django.shortcuts import render
from security.forms import *

from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.
def index(request):
    return render(request,'security/index.html')

@login_required
def special(request):
    return render(request,'security/special.html')
    # return HttpResponse('You are logged in!')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
def register(request):
    registered=False

    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)
    
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            # define the onetoone relation btwn UserProfileInfo class and User class
            profile.user=user

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']
            profile.save()

            registered=True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()
    return render(request,'security/registration.html',
    {
        'user_form':user_form,
        'profile_form':profile_form,
        'registered':registered
    })

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE") 
        else:
            print("someone tried login and failed.")
            print(username," ",password)
            return HttpResponse("invalid login details")
    else:
        return render(request,'security/login.html',{})      