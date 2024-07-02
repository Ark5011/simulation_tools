from django.contrib import admin
from .models import Gt
from import_export.admin import ImportExportModelAdmin

myModels = [Gt]
admin.site.register(myModels, ImportExportModelAdmin)
# Register your models here.
