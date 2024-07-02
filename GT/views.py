from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .forms import Gtform
from .models import Gt

# Create your views here.
def gt_form(request):
    context = {
        'Donald': 'Duck',
    }
    return render(request, 'GT/index.html', context)

def exportFile(request):
    pass
