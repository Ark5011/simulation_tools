from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'home/fail.html')
    else:
        form = CreateUserForm()
        context = {'registerform': form}
        return render(request, 'home/register.html', context)
    
    
def user_login(request):
    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')
        project = request.POST.get('project')
        factory = request.POST.get('factory')
        line = request.POST.get('line')
        product = request.POST.get('product')
        location = request.POST.get('location')
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            context = {'project': project, 'factory': factory, 'line': line, 'product': product, 'location': location}
            request.session['user_info'] = [context]
            return redirect('home')
        else:
            messages.error(request, name + password)
            return redirect('login')
    else:
        return render(request, 'home/login.html')
    
    
def logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    return render(request, 'home/homev2.html')

