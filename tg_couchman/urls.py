from django.urls import path
from . import views

app_name = 'tg_couchman'

urlpatterns = [
    path('', views.tg_form, name='tg_form'),
    path('export/', views.exportFile, name='exportFile'),
]