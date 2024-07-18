from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:login')
        else:
            messages.info(request, 'Registration Failed!')
            return redirect('home:register')
    else:
        form = CreateUserForm()
        context = {'registerform': form}
        return render(request, 'home/register.html', context)
    
    
def user_login(request):
    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('home:homepage')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('home:login')
    else:
        return render(request, 'home/login.html')
    
    
def logout_view(request):
    logout(request)
    return redirect('home:login')

def update_session_variable(request):
    if request.method == 'POST':
        new_value = request.POST.get('new_value')
        if new_value:
            new_value = list(new_value.split(','))
            context = {'project': new_value[0], 'factory': new_value[1], 'line': new_value[2], 'product': new_value[3], 'location': new_value[4]}
            request.session['user_info'] = context
            return HttpResponse({'status': 'success'})
        else:
            return HttpResponse({'status': 'error', 'message': 'No value provided'})

    return HttpResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required(login_url='home:login')
def homepage(request):
    return render(request, 'home/homev2.html')

@login_required(login_url='home:login')
def archive(request):
    return render(request, 'home/archive.html')