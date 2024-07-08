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
            f_min = tg_data['zipped_min'][0][3]
            f_target = tg_data['zipped_target'][0][3]
            f_max = tg_data['zipped_max'][0][3]     
            tg_min = tg_data['tg_min']
            tg_target = tg_data['tg_target']
            tg_max = tg_data['tg_max']
            
            aw_min = form.cleaned_data['aw_min']
            aw_target = form.cleaned_data['aw_target']
            aw_max = form.cleaned_data['aw_max']
            aw_actual = form.cleaned_data['aw_actual']
            aw_sample = form.cleaned_data['aw_sample']
            w_actual = form.cleaned_data['w_actual']
            w_sample = form.cleaned_data['w_sample']
            tg_actual = form.cleaned_data['tg_actual']
            tg_sample = form.cleaned_data['tg_sample']
            spraydry_min = form.cleaned_data['spraydry_min']
            spraydry_target = form.cleaned_data['spraydry_target']
            spraydry_max = form.cleaned_data['spraydry_max']
            sfb_min = form.cleaned_data['sfb_min']
            sfb_target = form.cleaned_data['sfb_target']
            sfb_max = form.cleaned_data['sfb_max']
            tg_dry = form.cleaned_data['tg_dry']
            k = form.cleaned_data['k']
            
            min_conc = (100-f_min)/100
            target_conc = (100-f_target)/100
            max_conc = (100-f_max)/100
            actual_conc = (100-w_actual)/100
            sample_conc = (100-w_sample)/100
            
            #Tg G&T = [C*Tg_dry + K(1-C)(-135)]/[C + K(1-C)]
            tg_gt_min = (min_conc*tg_dry + k*(1-min_conc)*(-135))/(min_conc + k*(1-min_conc))
            tg_gt_target = (target_conc*tg_dry + k*(1-target_conc)*(-135))/(target_conc + k*(1-target_conc))
            tg_gt_max = (max_conc*tg_dry + k*(1-max_conc)*(-135))/(max_conc + k*(1-max_conc))
            tg_gt_actual = (actual_conc*tg_dry + k*(1-actual_conc)*(-135))/(actual_conc + k*(1-actual_conc))
            tg_gt_sample = (sample_conc*tg_dry + k*(1-sample_conc)*(-135))/(sample_conc + k*(1-sample_conc))
            
            graph_x0 = (1*tg_dry + k*(1-1)*(-135))/(1 + k*(1-1))
            graph_x1 = (0.99*tg_dry + k*(1-0.99)*(-135))/(0.99 + k*(1-0.99))
            graph_x2 = (0.98*tg_dry + k*(1-0.98)*(-135))/(0.98 + k*(1-0.98))
            graph_x3 = (0.97*tg_dry + k*(1-0.97)*(-135))/(0.97 + k*(1-0.97))
            graph_x4 = (0.96*tg_dry + k*(1-0.96)*(-135))/(0.96 + k*(1-0.96))
            graph_x5 = (0.95*tg_dry + k*(1-0.95)*(-135))/(0.95 + k*(1-0.95))
            graph_x6 = (0.94*tg_dry + k*(1-0.94)*(-135))/(0.94 + k*(1-0.94))
            graph_yvalues = [graph_x0, graph_x1, graph_x2, graph_x3, graph_x4, graph_x5, graph_x6]
               
            context = {
                'f_min': f_min,
                'f_target': f_target,
                'f_max': f_max,
                'tg_min': tg_min,
                'tg_target': tg_target,
                'tg_max': tg_max,
                
                'aw_min': aw_min,
                'aw_target': aw_target,
                'aw_max': aw_max,
                'aw_actual': aw_actual,
                'aw_sample': aw_sample,
                'w_actual': w_actual,
                'w_sample': w_sample,
                'tg_actual': tg_actual,
                'tg_sample': tg_sample,                
                'spraydry_min': spraydry_min,
                'spraydry_target': spraydry_target,
                'spraydry_max': spraydry_max,
                'sfb_min': sfb_min,
                'sfb_target': sfb_target,
                'sfb_max': sfb_max,
                'tg_dry': tg_dry,
                'k': k,
                
                'tg_gt_min': tg_gt_min,
                'tg_gt_target': tg_gt_target,
                'tg_gt_max': tg_gt_max,
                'tg_gt_actual': tg_gt_actual,
                'tg_gt_sample': tg_gt_sample,
                
                'graph_yvalues': graph_yvalues,
            }
            
            return render(request, 'GT/result.html', context)
        
    form = Gtform()
    return render(request, 'GT/index.html', {'form': form})

def exportFile(request):
    pass
