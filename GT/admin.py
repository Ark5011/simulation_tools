from django.contrib import admin
from .models import Gt, Graph_tg, Graph_w

myModels = [Gt, Graph_tg, Graph_w]
admin.site.register(myModels)
# Register your models here.
