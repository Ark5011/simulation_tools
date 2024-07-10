from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import TotalSolidsCalculation, TotalSolidsResult

def index(request):
    return render(request, 'ts_fe.html', {'input_data': {}})

def totalsolids(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            fat_content = float(data['fat_content'])
            start_density = float(data['density'])

            results = []

            calculation = TotalSolidsCalculation.objects.create(
                fat_content=fat_content,
                start_density=start_density
            )

            for i in range(61):
                current_density = start_density + i
                total_solids = (138.2 - (136.206 / current_density * 1000)) / (0.505 - (0.00651101 * fat_content))
                results.append(total_solids)
                TotalSolidsResult.objects.create(
                    calculation=calculation,
                    iteration=i,
                    density=current_density,
                    total_solids=total_solids
                )

            request.session['calculated_data_ts'] = {
                'fat_content': fat_content,
                'density': start_density,
                'total_solids': results,
            }

            return JsonResponse({
                'total_solids': results,
                'error': None
            })
        except (ValueError, KeyError) as e:
            return JsonResponse({'error': f"An error occurred: {e}"})
