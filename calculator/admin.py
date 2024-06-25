from django.contrib import admin
from .models import Tg, Cp, Formulation

myModels = [Tg, Cp, Formulation]
admin.site.register(myModels)
# Register your models here.
