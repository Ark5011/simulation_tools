from django.urls import path
from . import views

app_name = 'mass_balance'

urlpatterns = [
    path('', views.index, name='index'),
    path('mass_balance_tool/', views.mass_balance_tool, name='mass_balance_tool'),
    path('download_excel/', views.download_excel, name='download_excel'),
]