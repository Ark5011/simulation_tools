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
            'hambient': format_value(hambient, "{:,.2f}"),
            'g1': format_value(g1, "{:,.0f}"),
            'tinlet': format_value(tinlet, "{:,.1f}"),
            'toutlet': format_value(toutlet, "{:,.1f}"),
            'tavg1': format_value(tavg1, "{:,.1f}"),
            'cp1': format_value(cp1, "{:,.3f}"),
            'dh1': format_value(dh1, "{:,.1f}"),
            'g2': format_value(data['sfbair'], "{:,.0f}"),
            'tsfbin': format_value(data['sfbinletT'], "{:,.1f}"),
            'tavg2': format_value(tavg2, "{:,.1f}"),
            'cp2': format_value(cp2, "{:,.3f}"),
            'dh2': format_value(dh2, "{:,.1f}"),
            'g3': format_value(data['roofcoolingair'], "{:,.0f}"),
            'troof': format_value(data['roofcoolingT'], "{:,.1f}"),
            'tavg3': format_value(tavg3, "{:,.1f}"),
            'cp3': format_value(cp3, "{:,.1f}"),
            'dh3': format_value(dh3, "{:,.1f}"),
            'a': format_value(a, "{:,.1f}"),
            'tfeed': format_value(tfeed, "{:,.1f}"),
            'cpwater': format_value(cpwater, "{:,.3f}"),
            'hwater': format_value(hwater, "{:,.2f}"),
            'b': format_value(b, "{:,.2f}"),
            'evaporation': format_value(evaporation, "{:,.2f}"),
            'solids_flowrate': format_value(solids_flowrate, "{:,.2f}"),
            'powder_rate': format_value(powder_rate, "{:,.2f}"),
            'total_water_vapour_flowrate': format_value(total_water_vapour_flowrate, "{:,.2f}"),
            'total_outlet_airflow': format_value(total_outlet_airflow, "{:,.1f}"),
            'houtlet': format_value(houtlet, "{:,.2f}"),
            'pbaro_1': format_value(pbaro_1, "{:,.2f}"),
            'v_1': format_value(v_1, "{:,.3f}"),
            'w_1': format_value(w_1, "{:,.1f}"),
            'rh_1': format_value(rh_1, "{:,.3f}"),
            'pbaro_2': format_value(pbaro_2, "{:,.2f}"),
            'v_2': format_value(v_2, "{:,.3f}"),
            'w_2': format_value(w_2, "{:,.3f}"),
            'sfb_v': format_value(sfb_v, "{:,.3f}"),
            'sfb_w': format_value(sfb_w, "{:,.2f}"),
            'sfb_rh': format_value(sfb_rh, "{:,.3f}"),
            'w1': format_value(w1, "{:,.3f}"),
            'w2': format_value(w2, "{:,.3f}"),
            'w3': format_value(w3, "{:,.3f}"),
            'w4': format_value(w4, "{:,.3f}"),
            'altitude_feet': format_value(altitude_feet, "{:,.3f}"),
            'error': None
        }

            return JsonResponse(response_data)

        else:
            return JsonResponse({'error': 'Invalid request method.'}, status=405)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def generate_excel(request):
    try:
        # Retrieve form data from POST request (assuming form is submitted via POST)
        if request.method == 'POST':
            data_from_html = {key: request.POST.get(key, '') for key in request.POST}

            # Simulating data retrieval from session (replace with actual data fetching logic)
            data_from_mbtool = request.session.get('calculated_data', {})

            # Prepare Excel data with the specified variables
            excel_data = [
                ['Humidities'],
                ['Primary Air AH', data_from_html.get('primaryairAH', ''), 'g/kg'],
                ['SFB Inlet AH', data_from_html.get('sfbinletAH', ''), 'g/kg'],
                ['SFB Inlet RH', round(data_from_mbtool.get('sfb_inlet_rh', 0), 2), '%'],
                ['Outlet Air AH', round(data_from_mbtool.get('outlet_air_ah', 0), 2), 'g/kg'],
                ['Outlet Air RH', round(data_from_mbtool.get('outlet_air_rh', 0), 2), '%'],
                ['Dummy Outlet Air RH', round(data_from_mbtool.get('dummy_outlet_air_rh', 0), 2), 'g/kg'],
                [' '],
                ['Temperatures'],
                ['Primary Inlet T', data_from_html.get('primaryinletT', ''), '%'],
                ['SFB Inlet T', data_from_html.get('sfbinletT', ''), 'g/kg'],
                ['Roof Cooling T', data_from_html.get('roofcoolingT', ''), '°C'],
                ['Outlet Air T', data_from_html.get('outletairT', ''), '°C'],
                ['Dummy Outlet Air T', round(data_from_mbtool.get('dummy_outlet_air_t', 0), 2), '°C'],
                [' '],
                ['Airflows'],
                ['Primary Air', data_from_html.get('primaryair', ''), 'kg/h'],
                ['SFB Air', data_from_html.get('sfbair', ''), 'kg/h'],
                ['Roof Cooling Air', data_from_html.get('roofcoolingair', ''), 'kg/h'],
                ['Altitude', data_from_html.get('altitude', ''), 'm'],
                ['Barometric Pressure', round(data_from_mbtool.get('barometric_pressure', 0), 2), 'kPa'],
                [' '],
                ['Concentrate'],
                ['Total Solids', data_from_html.get('totalsolids', ''), '%'],
                ['Temperature', data_from_html.get('temperature', ''), '°C'],
                [' '],
                ['Powder'],
                ['Moisture (target)', data_from_html.get('moisture', ''), '%'],
                ['Production Rate', round(data_from_mbtool.get('production_rate', 0), 2), 'kg/h'],
                [' '],
                ['Tsticky (Estimated)', data_from_html.get('tsticky', ''), '°C']
            ]

            # Create an Excel workbook and sheet
            wb = Workbook()
            ws = wb.active
            ws.title = "Mass Balance Data"

            # Write the data to the Excel sheet
            for row in excel_data:
                ws.append(row)

            # Save the workbook to a bytes buffer
            output = BytesIO()
            wb.save(output)
            output.seek(0)

            # Create a response with the Excel data
            response = HttpResponse(
                output,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=mass_balance.xlsx'
            return response

        # If GET request, display a form or return a message
        return HttpResponse("Please submit the form to generate the Excel file.")

    except (ValueError, KeyError) as e:
        return HttpResponse(f"An error occurred: {e}", status=400)