from django.contrib import admin
from .models import Gt_input
from import_export.admin import ImportExportModelAdmin

myModels = [Gt_input]
admin.site.register(myModels, ImportExportModelAdmin)
# Register your models here.
