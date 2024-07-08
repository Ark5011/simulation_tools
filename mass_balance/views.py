from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from openpyxl import Workbook
import os
import math

# Replace with your preferred method to generate a secret key
SECRET_KEY = os.urandom(24)

def index(request):
    return render(request, 'mass_balance_fe.html', {'input_data': {}})

def format_value(value, fmt):
    return fmt.format(value) if isinstance(value, (float, int)) else value

@csrf_exempt
def mass_balance_tool(request):
    try:
        if request.method == 'POST':
            default_values = {
                'primaryairAH': 0.0,
                'primaryair': 0.0,
                'primaryinletT': 0.0,
                'outletairT': 0.0,
                'sfbair': 0.0,
                'sfbinletT': 0.0,
                'roofcoolingair': 0.0,
                'roofcoolingT': 0.0,
                'temperature': 0.0,
                'altitude': 0.0,
                'totalsolids': 0.0,
                'moisture': 0.0,
                'sfbinletAH': 0.0
            }

            data = {}
            for key, default in default_values.items():
                value = request.POST.get(key, '')
                data[key] = float(value) if value else default

            barometric_pressure = 0.0507 * (data['altitude'] / 304.8)**2 - 3.6564 * (data['altitude'] / 304.8) + 101.32
            hambient = data['primaryairAH']
            g1 = data['primaryair']
            tinlet = data['primaryinletT']
            toutlet = data['outletairT']
            tavg1 = (tinlet + toutlet) / 2
            cp1 = 1.0037 + 0.000032 * tavg1 + 0.00000036 * tavg1**2
            dh1 = g1*(tinlet-toutlet)*cp1
            g2 = data['sfbair']
            tsfbin = data['sfbinletT']
            tavg2 = (tsfbin + toutlet)/2
            cp2 = 1.0037 + 0.000032 * tavg2 + 0.00000036 * tavg2**2
            dh2 = g2*(tsfbin-toutlet)*cp2
            g3 = data['roofcoolingair']
            troof = data['roofcoolingT']
            tavg3 = (troof + toutlet)/2
            cp3 = 1.0037 + 0.000032 * tavg3 + 0.00000036 * tavg3**2
            dh3 = g3 * (troof-toutlet)*cp3
            tfeed = data['temperature']
            cpwater = 4.219
            hwater = 2256.70
            a = dh1 + dh2 + dh3
            b = 2256.7 + 4.219 * (100 - tfeed)
            evaporation = a / b
            w1 = data['primaryair'] * data['primaryairAH'] / 1000
            w2 = data['sfbinletAH'] * data['sfbair'] / 1000
            w3 = data['primaryairAH'] * data['roofcoolingair'] / 1000
            w4 = evaporation
            total_water_vapour_flowrate = w1 + w2 + w3 + w4
            total_outlet_airflow = data['primaryair'] + data['sfbair'] + data['roofcoolingair']
            outlet_air_absolute_humidity = 1000 * total_water_vapour_flowrate / total_outlet_airflow
            solids_flowrate = data['totalsolids'] * evaporation / (100 - data['totalsolids'] - (data['totalsolids'] * data['moisture']) / (100 - data['moisture']))
            powder_rate = solids_flowrate + solids_flowrate * data['moisture'] / (100 - data['moisture'])
            production_rate = powder_rate
            cross_checking = (production_rate - 25) / 25 * 100
            houtlet = outlet_air_absolute_humidity
            pbaro_1 = barometric_pressure
            v_1 = 23.2906 - (3882.07 / (229.93 + data['outletairT']))
            w_1 = math.exp(v_1)
            rh_1 = houtlet * 100 * pbaro_1 / (houtlet / 1000 + 0.622065) / w_1
            tdummy = data['outletairT'] - (data['sfbair'] / (data['primaryair'] + data['sfbair']) * (data['sfbinletT'] - data['outletairT']))
            pbaro_2 = 101.325
            v_2 = 23.2906 - (3882.07 / (229.93 + tdummy))
            w_2 = math.exp(v_2)
            rh_2 = houtlet * 100 * pbaro_2 / (tdummy / 1000 + 0.622065) / w_2
            sfb_v = 23.2906 - (3882.07 / (229.93 + data['sfbinletT']))
            sfb_w = math.exp(sfb_v)
            sfb_rh = data['sfbinletAH'] * 100 * pbaro_1 / ((data['sfbinletAH'] / 1000 + 0.622065) * sfb_w)
            altitude = data['altitude']
            altitude_feet = altitude / 304.8

            request.session['calculated_data'] = {
                'sfb_inlet_rh': sfb_rh,
                'outlet_air_ah': outlet_air_absolute_humidity,
                'outlet_air_rh': rh_1,
                'dummy_outlet_air_rh': rh_2,
                'dummy_outlet_air_t': tdummy,
                'production_rate': production_rate,
                'barometric_pressure': barometric_pressure,
                'primary_air_AH': data['primaryairAH'],
                'sfb_inlet_AH': data['sfbinletAH'],
                'primary_inlet_T': data['primaryinletT'],
                'sfb_inlet_T': data['sfbinletT'],
                'roof_cooling_T': data['roofcoolingT'],
                'outlet_air_T': data['outletairT'],
                'altitude': data['altitude'],
                'total_solids': data['totalsolids'],
                'temperature': data['temperature'],
                'moisture': data['moisture']
            }

            response_data = {
                'input_data': {key: "{:,.3f}".format(value) if isinstance(value, float) else value for key, value in data.items()},
                'sfb_inlet_rh': format_value(sfb_rh, "{:,.2f}"),
                'outlet_air_ah': format_value(outlet_air_absolute_humidity, "{:,.2f}"),
                'outlet_air_absolute_humidity': format_value(outlet_air_absolute_humidity, "{:,.2f}"),
                'outlet_air_rh': format_value(rh_1, "{:,.2f}"),
                'dummy_outlet_air_rh': format_value(rh_2, "{:,.2f}"),
                'dummy_outlet_air_t': format_value(tdummy, "{:,.2f}"),
                'tdummy': format_value(tdummy, "{:,.2f}"),
                'production_rate': format_value(production_rate, "{:,.2f}"),
                'barometric_pressure': format_value(barometric_pressure, "{:,.2f}"),
                'cross_checking': format_value(cross_checking, "{:,.2f}"),
                'primary_air_AH': format_value(data['primaryairAH'], "{:,.2f}"),
                'sfb_inlet_AH': format_value(data['sfbinletAH'], "{:,.2f}"),
                'primary_inlet_T': format_value(data['primaryinletT'], "{:,.2f}"),
                'sfb_inlet_T': format_value(data['sfbinletT'], "{:,.2f}"),
                'roof_cooling_T': format_value(data['roofcoolingT'], "{:,.2f}"),
                'outlet_air_T': format_value(data['outletairT'], "{:,.2f}"),
                'altitude': format_value(data['altitude'], "{:,.2f}"),
                'total_solids': format_value(data['totalsolids'], "{:,.2f}"),
                'temperature': format_value(data['temperature'], "{:,.2f}"),
                'moisture': format_value(data['moisture'], "{:,.2f}")
            }

            return JsonResponse(response_data)

        else:
            return JsonResponse({'error': 'Invalid request method.'}, status=405)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def download_excel(request):
    data = request.session.get('calculated_data', None)
    if data:
        wb = Workbook()
        ws = wb.active
        for key, value in data.items():
            ws.append([key, value])
        excel_data = BytesIO()
        wb.save(excel_data)
        excel_data.seek(0)
        response = HttpResponse(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=calculated_data.xlsx'
        return response
    else:
        return HttpResponse("No calculated data found.", status=404)
