from django.contrib import admin
from .models import Gt, Graph_tg, Graph_w
from import_export.admin import ImportExportModelAdmin

myModels = [Gt, Graph_tg, Graph_w]
admin.site.register(myModels, ImportExportModelAdmin)
# Register your models here.
