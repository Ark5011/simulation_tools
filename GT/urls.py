from django.urls import path
from . import views

app_name = 'GT'

urlpatterns = [
    path('', views.gt_form, name='gt_form'),
    path('export/', views.exportFile, name='exportFile'),
]