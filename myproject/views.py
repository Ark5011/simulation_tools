from django.shortcuts import render, redirect
from .forms import Projectform, CreateUserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CreateUserForm()
        context = {'registerform': form}
        return render(request, 'register.html', context)
    
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('project')
            else:
                return redirect('login')
    else:
        form = LoginForm()
        context = {'loginform': form}
        return render(request, 'login.html', context)
    
def logout(request):
    logout(request)
    return redirect('login')


def project_info(request):
    if request.method == "POST":
        form = Projectform(request.POST)
        if form.is_valid():
            #formulation values
            return render(request, 'home.html', {'form': form})
    else:
        form = Projectform()
        return render(request, 'home.html', {'form': form})

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

