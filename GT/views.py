from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .forms import Gtform
from .models import Gt, Graph_tg, Graph_w

# Create your views here.
def gt_form(request):
    x_values = Graph_w.objects.values_list('W', flat=True)
    y_values = Graph_tg.objects.values_list('Tg', flat=True)
    x_values = list(x_values)
    y_values = list(y_values)
    
    context = {
        'x_values': x_values,
        'y_values': y_values,
    }
    return render(request, 'GT/index.html', context)

def exportFile(request):
    pass
