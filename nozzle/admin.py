from django.contrib import admin
from .models import NozzleCalculation, NozzleTDResult, NozzleTDLResult

myModels = [NozzleCalculation, NozzleTDResult, NozzleTDLResult]
admin.site.register(myModels)
# Register your models here.
