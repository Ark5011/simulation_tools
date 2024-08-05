from django.urls import path
from . import views

app_name = 'GT'

urlpatterns = [
    path('', views.gt_form, name='gt_form'),
    path('excel/', views.generate_excel, name='excel'),
    path('pdf/', views.generate_pdf, name='result'),
]