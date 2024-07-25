from django.contrib import admin
from .models import InputData, CalculatedData

@admin.register(InputData)
class InputDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'primaryairAH', 'primaryair', 'primaryinletT', 'outletairT', 'sfbair', 'sfbinletT')
    search_fields = ('id',)

@admin.register(CalculatedData)
class CalculatedDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'input_data', 'sfb_inlet_rh', 'outlet_air_ah', 'outlet_air_rh', 'dummy_outlet_air_rh')
    search_fields = ('id', 'input_data__id')