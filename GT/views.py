from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .forms import Gtform
from .models import Gt_input

# Create your views here.
def gt_form(request):
    if request.method == "POST":
        form = Gtform(request.POST)
        if form.is_valid():
            tg_data = request.session['tg_data']
            f_min = tg_data['zipped_min'][3][0]
            f_target = tg_data['zipped_target'][3][0]
            f_max = tg_data['zipped_max'][3][0]     
            tg_min = tg_data['tg_min']
            tg_target = tg_data['tg_target']
            tg_max = tg_data['tg_max']   
            context = {
                'Donald': 'Duck',
            }
    return render(request, 'GT/index.html', context)

def exportFile(request):
    pass
