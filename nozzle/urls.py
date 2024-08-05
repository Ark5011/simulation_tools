from django.urls import path
from . import views

app_name = 'nozzle'

urlpatterns = [
    path('', views.index, name='index'),
    path('td/', views.td, name='td'),
    path('tdl/', views.tdl, name='tdl'),
]