from django.contrib import admin
from .models import Formulation

myModels = [Formulation]
admin.site.register(myModels)
# Register your models here.
