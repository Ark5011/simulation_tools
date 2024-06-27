from django.shortcuts import render
from django.views import View
from .forms import TgForm
from .models import Tg, Cp, Formulation

# Create your views here.
class Index(View):
    def get(self, request):
        form = TgForm()
        return render(request, 'simulation_tools/index.html', {'form': form})

    def post(self, request):
        form = TgForm(request.POST)
        if form.is_valid():
            #formulation values
            f_water_min = form.cleaned_data['water_min']
            f_water_target = f_water_min + 0.25
            f_water_max = f_water_target + 0.25
            
            f_casein = form.cleaned_data['casein']
            f_whey_protein = form.cleaned_data['whey_protein']
            f_GOS = form.cleaned_data['GOS']
            f_PDX = form.cleaned_data['PDX']
            f_lactose = 50.9 - f_GOS - f_PDX
            
            f_sum_min = sum([f_water_min, f_casein, f_whey_protein, f_lactose, f_GOS, f_PDX])
            f_sum_target = sum([f_water_target, f_casein, f_whey_protein, f_lactose, f_GOS, f_PDX])
            f_sum_max = sum([f_water_max, f_casein, f_whey_protein, f_lactose, f_GOS, f_PDX])
            
            #Wi values
            wi_water_min = f_water_min * 100 / 64.79
            wi_water_target = f_water_target * 100 / 64.79
            wi_water_max = f_water_max * 100 / 64.79
            
            wi_casein = f_casein * 100 / 64.79
            wi_whye_protein = f_whey_protein * 100 / 64.79
            wi_lactose = f_lactose * 100 / 64.79
            wi_GOS = f_GOS * 100 / 64.79
            wi_PDX = f_PDX * 100 / 64.79
            
            wi_sum_min = sum([wi_water_min, wi_casein, wi_whye_protein, wi_lactose, wi_GOS, wi_PDX])
            wi_sum_target = sum([wi_water_target, wi_casein, wi_whye_protein, wi_lactose, wi_GOS, wi_PDX])
            wi_sum_max = sum([wi_water_max, wi_casein, wi_whye_protein, wi_lactose, wi_GOS, wi_PDX])
            
            #Cp * Wi values
            cp_values = Cp.objects.all()
            cpwi_water_min = wi_water_min * cp_values[0].water
            cpwi_water_target = wi_water_target * cp_values[0].water
            cpwi_water_max = wi_water_max * cp_values[0].water
            
            cpwi_casein = wi_casein * cp_values[0].casein
            cpwi_whye_protein = wi_whye_protein * cp_values[0].whey_protein
            cpwi_lactose = wi_lactose * cp_values[0].lactose
            cpwi_GOS = wi_GOS * cp_values[0].GOS
            cpwi_PDX = wi_PDX * cp_values[0].PDX
            
            cpwi_sum_min = sum([cpwi_water_min, cpwi_casein, cpwi_whye_protein, cpwi_lactose, cpwi_GOS, cpwi_PDX])
            cpwi_sum_target = sum([cpwi_water_target, cpwi_casein, cpwi_whye_protein, cpwi_lactose, cpwi_GOS, cpwi_PDX])
            cpwi_sum_max = sum([cpwi_water_max, cpwi_casein, cpwi_whye_protein, cpwi_lactose, cpwi_GOS, cpwi_PDX])
            
            #Cp * Wi * Tg values
            tg_values = Tg.objects.all()
            cpwitg_water_min = cpwi_water_min * tg_values[0].water
            cpwitg_water_target = cpwi_water_target * tg_values[0].water
            cpwitg_water_max = cpwi_water_max * tg_values[0].water
            
            cpwitg_casein = cpwi_casein * tg_values[0].casein
            cpwitg_whye_protein = cpwi_whye_protein * tg_values[0].whey_protein
            cpwitg_lactose = cpwi_lactose * tg_values[0].lactose
            cpwitg_GOS = cpwi_GOS * tg_values[0].GOS
            cpwitg_PDX = cpwi_PDX * tg_values[0].PDX
            
            cpwitg_sum_min = sum([cpwitg_water_min, cpwitg_casein, cpwitg_whye_protein, cpwitg_lactose, cpwitg_GOS, cpwitg_PDX])
            cpwitg_sum_target = sum([cpwitg_water_target, cpwitg_casein, cpwitg_whye_protein, cpwitg_lactose, cpwitg_GOS, cpwitg_PDX])
            cpwitg_sum_max = sum([cpwitg_water_max, cpwitg_casein, cpwitg_whye_protein, cpwitg_lactose, cpwitg_GOS, cpwitg_PDX])
            
            final_tg_min = cpwitg_sum_min / cpwi_sum_min
            final_tg_target = cpwitg_sum_target / cpwi_sum_target
            final_tg_max = cpwitg_sum_max / cpwi_sum_max
            
            ingredients = ['Water', 'Casein', 'Whey Protein', 'Lactose', 'GOS', 'PDX', 'Sum']
            tg_values = [tg_values[0].water, tg_values[0].casein, tg_values[0].whey_protein, tg_values[0].lactose, tg_values[0].GOS, tg_values[0].PDX, 0]
            tg_values = [round(x,3) for x in tg_values]
            cp_values = [cp_values[0].water, cp_values[0].casein, cp_values[0].whey_protein, cp_values[0].lactose, cp_values[0].GOS, cp_values[0].PDX, 0]
            cp_values = [round(x,3) for x in cp_values]
            
            f_values_min = [f_water_min, f_casein, f_whey_protein, f_lactose, f_GOS, f_PDX, f_sum_min]
            f_values_min = [round(x,3) for x in f_values_min]
            f_values_target = [f_water_target, f_casein, f_whey_protein, f_lactose, f_GOS, f_PDX, f_sum_target]
            f_values_target = [round(x,3) for x in f_values_target]
            f_values_max = [f_water_max, f_casein, f_whey_protein, f_lactose, f_GOS, f_PDX, f_sum_max]
            f_values_max = [round(x,3) for x in f_values_max]
            
            wi_values_min = [wi_water_min, wi_casein, wi_whye_protein, wi_lactose, wi_GOS, wi_PDX, wi_sum_min]
            wi_values_min = [round(x,3) for x in wi_values_min]
            wi_values_target = [wi_water_target, wi_casein, wi_whye_protein, wi_lactose, wi_GOS, wi_PDX, wi_sum_target]
            wi_values_target = [round(x,3) for x in wi_values_target]
            wi_values_max = [wi_water_max, wi_casein, wi_whye_protein, wi_lactose, wi_GOS, wi_PDX, wi_sum_max]
            wi_values_max = [round(x,3) for x in wi_values_max]
            
            cpwi_values_min = [cpwi_water_min, cpwi_casein, cpwi_whye_protein, cpwi_lactose, cpwi_GOS, cpwi_PDX, cpwi_sum_min]
            cpwi_values_min = [round(x,3) for x in cpwi_values_min]
            cpwi_values_target = [cpwi_water_target, cpwi_casein, cpwi_whye_protein, cpwi_lactose, cpwi_GOS, cpwi_PDX, cpwi_sum_target]
            cpwi_values_target = [round(x,3) for x in cpwi_values_target]
            cpwi_values_max = [cpwi_water_max, cpwi_casein, cpwi_whye_protein, cpwi_lactose, cpwi_GOS, cpwi_PDX, cpwi_sum_max]
            cpwi_values_max = [round(x,3) for x in cpwi_values_max]
            
            cpwitg_values_min = [cpwitg_water_min, cpwitg_casein, cpwitg_whye_protein, cpwitg_lactose, cpwitg_GOS, cpwitg_PDX, cpwitg_sum_min]
            cpwitg_values_min = [round(x,3) for x in cpwitg_values_min]
            cpwitg_values_target = [cpwitg_water_target, cpwitg_casein, cpwitg_whye_protein, cpwitg_lactose, cpwitg_GOS, cpwitg_PDX, cpwitg_sum_target]
            cpwitg_values_target = [round(x,3) for x in cpwitg_values_target]
            cpwitg_values_max = [cpwitg_water_max, cpwitg_casein, cpwitg_whye_protein, cpwitg_lactose, cpwitg_GOS, cpwitg_PDX, cpwitg_sum_max]
            cpwitg_values_max = [round(x,3) for x in cpwitg_values_max]
            
            final_tg_min_list = [""] * 6 + [round(final_tg_min,3)]
            final_tg_target_list = [""] * 6 + [round(final_tg_target,3)]
            final_tg_max_list = [""] * 6 + [round(final_tg_max,3)]
            
            zipped_min = zip(ingredients, tg_values, cp_values, f_values_min, wi_values_min, cpwi_values_min, cpwitg_values_min, final_tg_min_list)
            zipped_target = zip(ingredients, tg_values, cp_values, f_values_target, wi_values_target, cpwi_values_target, cpwitg_values_target, final_tg_target_list)
            zipped_max = zip(ingredients, tg_values, cp_values, f_values_max, wi_values_max, cpwi_values_max, cpwitg_values_max, final_tg_max_list)
            
            context = {
                'tg_min': round(final_tg_min,3),
                'tg_target': round(final_tg_target,3),
                'tg_max': round(final_tg_max,3),
                
                'zipped_min': zipped_min,
                'zipped_target': zipped_target,
                'zipped_max': zipped_max,
                         
            }
            
            return render(request, 'simulation_tools/result.html', context)
            
class Gt(View):
    def get(self, request):
        form = TgForm()
        return render(request, 'simulation_tools/index.html', {'form': form})