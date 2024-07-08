from django.urls import path
from .views import index, mass_balance_tool, download_excel

urlpatterns = [
    path('', index, name='index'),
    path('mass_balance_tool/', mass_balance_tool, name='mass_balance_tool'),
    path('download_excel/', download_excel, name='download_excel'),
]
