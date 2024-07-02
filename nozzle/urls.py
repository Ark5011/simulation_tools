from django.urls import path
from . import views

app_name = 'nozzle'

urlpatterns = [
    path('index/', views.NozzleCalculation, name='index'),
    path('td/', views.NozzleTDResult, name='td'),
    path('tdl/', views.NozzleTDLResult, name='tdl'),
]