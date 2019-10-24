from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from users.forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def SignUp(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
    else:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                messages.success(request, f'%s has been Created. Please, Login to continue' %form.cleaned_data['username'])
                form.save()
                return redirect('users:login')
        else:
            form = UserRegistrationForm()
        context = {'form':form, 'signup_page':'active'}
        return render(request, 'SignUp.html', context)

def Login(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
    else:
        if request.method == 'POST':
            form = UserLoginForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)                
                    return redirect('blog:home')

            else:
                print('Form invalid')
                pass
        else:
            form = UserLoginForm()
        context = {'form':form, 'login_page':'active'}
        return render(request, 'login.html', context)
    
def Logout(request):
    logout(request)
    return redirect("blog:home")