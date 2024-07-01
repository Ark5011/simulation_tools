from django.shortcuts import render
from .forms import Projectform

def project_info(request):
    if request.method == "POST":
        form = Projectform(request.POST)
        if form.is_valid():
            #formulation values
            return render(request, 'home.html', {'form': form})
    else:
        form = Projectform()
        return render(request, 'project.html', {'form': form})


def home(request):
    return render(request, 'home.html')