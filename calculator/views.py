from django.shortcuts import render
from django.views import View
from .forms import TgForm
from .models import Tg, Cp, Formulation

# Create your views here.
class Index(View):
    def get(self, request):
        form = TgForm()
        return render(request, 'calculator/index.html', {'form': form})

    def post(self, request):
        form = TgForm(request.POST)
        if form.is_valid():
            #formulation values
            f_water = form.cleaned_data['water']
            f_casein = form.cleaned_data['casein']
            f_whey_protein = form.cleaned_data['whey_protein']
            f_GOS = form.cleaned_data['GOS']
            f_PDX = form.cleaned_data['PDX']
            f_lactose = 50.9 - f_GOS - f_PDX
            f_sum = sum([f_water, f_casein, f_whey_protein, f_lactose, f_GOS, f_PDX])
            
            #Wi values
            wi_water = f_water * 100 / 64.79
            wi_casein = f_casein * 100 / 64.79
            wi_whye_protein = f_whey_protein * 100 / 64.79
            wi_lactose = f_lactose * 100 / 64.79
            wi_GOS = f_GOS * 100 / 64.79
            wi_PDX = f_PDX * 100 / 64.79
            wi_sum = sum([wi_water, wi_casein, wi_whye_protein, wi_lactose, wi_GOS, wi_PDX])
            
            #Cp * Wi values
            cp_values = Cp.objects.all()
            cpwi_water = wi_water * cp_values[0].water
            cpwi_casein = wi_casein * cp_values[0].casein
            cpwi_whye_protein = wi_whye_protein * cp_values[0].whey_protein
            cpwi_lactose = wi_lactose * cp_values[0].lactose
            cpwi_GOS = wi_GOS * cp_values[0].GOS
            cpwi_PDX = wi_PDX * cp_values[0].PDX
            cpwi_sum = sum([cpwi_water, cpwi_casein, cpwi_whye_protein, cpwi_lactose, cpwi_GOS, cpwi_PDX])
            
            #Cp * Wi * Tg values
            tg_values = Tg.objects.all()
            cpwitg_water = cpwi_water * tg_values[0].water
            cpwitg_casein = cpwi_casein * tg_values[0].casein
            cpwitg_whye_protein = cpwi_whye_protein * tg_values[0].whey_protein
            cpwitg_lactose = cpwi_lactose * tg_values[0].lactose
            cpwitg_GOS = cpwi_GOS * tg_values[0].GOS
            cpwitg_PDX = cpwi_PDX * tg_values[0].PDX
            cpwitg_sum = sum([cpwitg_water, cpwitg_casein, cpwitg_whye_protein, cpwitg_lactose, cpwitg_GOS, cpwitg_PDX])
            
            final_tg = cpwitg_sum / cpwi_sum
            
            context = {
                'tg': round(final_tg,3),
            }
            
            return render(request, 'calculator/result.html', context)
            
