from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import pandas as pd
from .forms import TgForm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# Create your views here.
@login_required(login_url='home:login')
def tg_form(request):
    if request.method == "POST":
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
            f_lactose = form.cleaned_data['lactose']
                
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
            cp_value = {'water':1.94, 'casein':0.26, 'whey_protein':0.09, 'lactose':0.38, 'gos':0.24, 'pdx':0.473}
            cpwi_water_min = wi_water_min * cp_value['water']
            cpwi_water_target = wi_water_target * cp_value['water']
            cpwi_water_max = wi_water_max * cp_value['water']
            
            cpwi_casein = wi_casein * cp_value['casein']
            cpwi_whye_protein = wi_whye_protein * cp_value['whey_protein']
            cpwi_lactose = wi_lactose * cp_value['lactose']
            cpwi_GOS = wi_GOS * cp_value['gos']
            cpwi_PDX = wi_PDX * cp_value['pdx']
            
            cpwi_sum_min = sum([cpwi_water_min, cpwi_casein, cpwi_whye_protein, cpwi_lactose, cpwi_GOS, cpwi_PDX])
            cpwi_sum_target = sum([cpwi_water_target, cpwi_casein, cpwi_whye_protein, cpwi_lactose, cpwi_GOS, cpwi_PDX])
            cpwi_sum_max = sum([cpwi_water_max, cpwi_casein, cpwi_whye_protein, cpwi_lactose, cpwi_GOS, cpwi_PDX])
            
            #Cp * Wi * Tg values
            tg_value = {'water':-135, 'casein':132, 'whey_protein':127, 'lactose':101, 'gos':31, 'pdx':63}
            cpwitg_water_min = cpwi_water_min * tg_value['water']
            cpwitg_water_target = cpwi_water_target * tg_value['water']
            cpwitg_water_max = cpwi_water_max * tg_value['water']
            
            cpwitg_casein = cpwi_casein * tg_value['casein']
            cpwitg_whye_protein = cpwi_whye_protein * tg_value['whey_protein']
            cpwitg_lactose = cpwi_lactose * tg_value['lactose']
            cpwitg_GOS = cpwi_GOS * tg_value['gos']
            cpwitg_PDX = cpwi_PDX * tg_value['pdx']
            
            cpwitg_sum_min = sum([cpwitg_water_min, cpwitg_casein, cpwitg_whye_protein, cpwitg_lactose, cpwitg_GOS, cpwitg_PDX])
            cpwitg_sum_target = sum([cpwitg_water_target, cpwitg_casein, cpwitg_whye_protein, cpwitg_lactose, cpwitg_GOS, cpwitg_PDX])
            cpwitg_sum_max = sum([cpwitg_water_max, cpwitg_casein, cpwitg_whye_protein, cpwitg_lactose, cpwitg_GOS, cpwitg_PDX])
            
            final_tg_min = cpwitg_sum_min / cpwi_sum_min
            final_tg_target = cpwitg_sum_target / cpwi_sum_target
            final_tg_max = cpwitg_sum_max / cpwi_sum_max
            
            ingredients = ['Water', 'Casein', 'Whey Protein', 'Lactose', 'GOS', 'PDX', 'Sum']
            tg_values = [tg_value['water'], tg_value['casein'], tg_value['whey_protein'], tg_value['lactose'], tg_value['gos'], tg_value['pdx'], '']
            cp_values = [cp_value['water'], cp_value['casein'], cp_value['whey_protein'], cp_value['lactose'], cp_value['gos'], cp_value['pdx'], '']
            
            f_values_min = [f_water_min, f_casein, f_whey_protein, f_lactose, f_GOS, f_PDX, f_sum_min]
            f_values_min_rounded = [round(x,3) for x in f_values_min]
            f_values_target = [f_water_target, f_casein, f_whey_protein, f_lactose, f_GOS, f_PDX, f_sum_target]
            f_values_target_rounded = [round(x,3) for x in f_values_target]
            f_values_max = [f_water_max, f_casein, f_whey_protein, f_lactose, f_GOS, f_PDX, f_sum_max]
            f_values_max_rounded = [round(x,3) for x in f_values_max]
            
            wi_values_min = [wi_water_min, wi_casein, wi_whye_protein, wi_lactose, wi_GOS, wi_PDX, wi_sum_min]
            wi_values_min_rounded = [round(x,3) for x in wi_values_min]
            wi_values_target = [wi_water_target, wi_casein, wi_whye_protein, wi_lactose, wi_GOS, wi_PDX, wi_sum_target]
            wi_values_target_rounded = [round(x,3) for x in wi_values_target]
            wi_values_max = [wi_water_max, wi_casein, wi_whye_protein, wi_lactose, wi_GOS, wi_PDX, wi_sum_max]
            wi_values_max_rounded = [round(x,3) for x in wi_values_max]
            
            cpwi_values_min = [cpwi_water_min, cpwi_casein, cpwi_whye_protein, cpwi_lactose, cpwi_GOS, cpwi_PDX, cpwi_sum_min]
            cpwi_values_min_rounded = [round(x,3) for x in cpwi_values_min]
            cpwi_values_target = [cpwi_water_target, cpwi_casein, cpwi_whye_protein, cpwi_lactose, cpwi_GOS, cpwi_PDX, cpwi_sum_target]
            cpwi_values_target_rounded = [round(x,3) for x in cpwi_values_target]
            cpwi_values_max = [cpwi_water_max, cpwi_casein, cpwi_whye_protein, cpwi_lactose, cpwi_GOS, cpwi_PDX, cpwi_sum_max]
            cpwi_values_max_rounded = [round(x,3) for x in cpwi_values_max]
            
            cpwitg_values_min = [cpwitg_water_min, cpwitg_casein, cpwitg_whye_protein, cpwitg_lactose, cpwitg_GOS, cpwitg_PDX, cpwitg_sum_min]
            cpwitg_values_min_rounded = [round(x,3) for x in cpwitg_values_min]
            cpwitg_values_target = [cpwitg_water_target, cpwitg_casein, cpwitg_whye_protein, cpwitg_lactose, cpwitg_GOS, cpwitg_PDX, cpwitg_sum_target]
            cpwitg_values_target_rounded = [round(x,3) for x in cpwitg_values_target]
            cpwitg_values_max = [cpwitg_water_max, cpwitg_casein, cpwitg_whye_protein, cpwitg_lactose, cpwitg_GOS, cpwitg_PDX, cpwitg_sum_max]
            cpwitg_values_max_rounded = [round(x,3) for x in cpwitg_values_max]
            
            final_tg_min_list = [""] * 6 + [round(final_tg_min,3)]
            final_tg_target_list = [""] * 6 + [round(final_tg_target,3)]
            final_tg_max_list = [""] * 6 + [round(final_tg_max,3)]
            
            zipped_min = list(zip(ingredients, tg_values, cp_values, f_values_min_rounded, wi_values_min_rounded, cpwi_values_min_rounded, cpwitg_values_min_rounded, final_tg_min_list))
            zipped_target = list(zip(ingredients, tg_values, cp_values, f_values_target_rounded, wi_values_target_rounded, cpwi_values_target_rounded, cpwitg_values_target_rounded, final_tg_target_list))
            zipped_max = list(zip(ingredients, tg_values, cp_values, f_values_max_rounded, wi_values_max_rounded, cpwi_values_max_rounded, cpwitg_values_max_rounded, final_tg_max_list))
            
            context = {
                'tg_min': round(final_tg_min,3),
                'tg_target': round(final_tg_target,3),
                'tg_max': round(final_tg_max,3),
                
                'zipped_min': zipped_min,
                'zipped_target': zipped_target,
                'zipped_max': zipped_max,
                            
            }
            
            zipped_min_raw = list(zip(ingredients, tg_values, cp_values, f_values_min, wi_values_min, cpwi_values_min, cpwitg_values_min, final_tg_min_list))
            zipped_target_raw = list(zip(ingredients, tg_values, cp_values, f_values_target, wi_values_target, cpwi_values_target, cpwitg_values_target, final_tg_target_list))
            zipped_max_raw = list(zip(ingredients, tg_values, cp_values, f_values_max, wi_values_max, cpwi_values_max, cpwitg_values_max, final_tg_max_list))
            
            context_raw = {
                'tg_min': final_tg_min,
                'tg_target': final_tg_target,
                'tg_max': final_tg_max,
                
                'zipped_min': zipped_min_raw,
                'zipped_target': zipped_target_raw,
                'zipped_max': zipped_max_raw,
            }
            
            request.session['tg_data'] = context_raw
            request.session['tg_data_rounded'] = context
            
            return render(request, 'tg_couchman/result.html', context)
    else:
        form = TgForm()
        return render(request, 'tg_couchman/index.html', {'form': form})

@login_required(login_url='home:login')    
def exportFile(request):
    tg_data = request.session['tg_data']
    
    excel_data = [
        ['Ingredients', 'Tg (C)', 'Cp (J/g/C)', 'Formulation (%)', 'Wi', 'Cp X Wi', 'Cp X Wi X Tg', 'Tg'],
    ]
    for ingredients, tg_values, cp_values, f_values_min, wi_values_min, cpwi_values_min, cpwitg_values_min, final_tg_min_list in tg_data['zipped_min']:
        row = [ingredients, tg_values, cp_values, f_values_min, wi_values_min, cpwi_values_min, cpwitg_values_min, final_tg_min_list]
        excel_data.append(row)
    
    excel_data.append([''])
    excel_data.append(['STAGE 3', '', '', 'Target Moisture'])
    excel_data.append(['Ingredients', 'Tg (C)', 'Cp (J/g/C)', 'Formulation (%)', 'Wi', 'Cp X Wi', 'Cp X Wi X Tg', 'Tg'])
    
    for ingredients, tg_values, cp_values, f_values_target, wi_values_target, cpwi_values_target, cpwitg_values_target, final_tg_target_list in tg_data['zipped_target']:
        row = [ingredients, tg_values, cp_values, f_values_target, wi_values_target, cpwi_values_target, cpwitg_values_target, final_tg_target_list]
        excel_data.append(row)
        
    excel_data.append([''])
    excel_data.append(['STAGE 3', '', '', 'Max Moisture'])
    excel_data.append(['Ingredients', 'Tg (C)', 'Cp (J/g/C)', 'Formulation (%)', 'Wi', 'Cp X Wi', 'Cp X Wi X Tg', 'Tg'])
    
    for ingredients, tg_values, cp_values, f_values_max, wi_values_max, cpwi_values_max, cpwitg_values_max, final_tg_max_list in tg_data['zipped_max']:
        row = [ingredients, tg_values, cp_values, f_values_max, wi_values_max, cpwi_values_max, cpwitg_values_max, final_tg_max_list]
        excel_data.append(row)
    
    df = pd.DataFrame(excel_data, columns=['STAGE 3', '', '', 'Min Moisture','','','',''])
    
    resp = HttpResponse(content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename=Tg_Couchman.csv'
    df.to_csv(path_or_buf=resp, sep=',', index=False)
    
    return resp

@login_required(login_url='home:login')
def generate_pdf(request):
    tg_data = request.session.get('tg_data_rounded')
    
    # Create a response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Tg_Couchman.pdf"'
    
    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title = Paragraph("Tg Couchman", styles['Heading1'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Function to create a table from the data
    def create_table(data, title):
        # Table headers
        headers = ["Ingredients", "Tg (C)", "Cp (J/g/C)", "Formulation (%)", "Wi", "Cp * Wi", "Cp * Wi * Tg", "Tg"]
        table_data = [headers]
        table_data.extend(data)
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONT_SIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ]))
        elements.append(Paragraph(title, styles['Heading2']))
        elements.append(table)
        elements.append(Spacer(1, 12))
    
    # Add tables for min, target, and max moisture with labels
    create_table(tg_data['zipped_min'], "Min moisture")
    create_table(tg_data['zipped_target'], "Target moisture")
    create_table(tg_data['zipped_max'], "Max moisture")
    
    if request.session['user_info']:
        user_info = request.session['user_info']
        elements.append(Spacer(1, 24))
        elements.append(Paragraph("User Information:", styles['Heading2']))
        elements.append(Paragraph(f"Name: {request.user.username}", styles['Normal']))
        elements.append(Paragraph(f"Project: {user_info['project']}", styles['Normal']))
        elements.append(Paragraph(f"Factory: {user_info['factory']}", styles['Normal']))
        elements.append(Paragraph(f"Line: {user_info['line']}", styles['Normal']))
        elements.append(Paragraph(f"Product: {user_info['product']}", styles['Normal']))
        elements.append(Paragraph(f"Location: {user_info['location']}", styles['Normal']))
    else:
        elements.append(Spacer(1, 24))
        elements.append(Paragraph("User Information: None", styles['Heading2']))
        elements.append(Paragraph("Re-Login to input User Information", styles['Normal']))
    
    # Build the document
    doc.build(elements)
    
    return response