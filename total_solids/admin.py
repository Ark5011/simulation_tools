from django.contrib import admin
from .models import TotalSolidsCalculation, TotalSolidsResult

class TotalSolidsResultInline(admin.TabularInline):
    model = TotalSolidsResult
    extra = 0

class TotalSolidsCalculationAdmin(admin.ModelAdmin):
    list_display = ('fat_content', 'start_density', 'created_at')
    inlines = [TotalSolidsResultInline]

admin.site.register(TotalSolidsCalculation, TotalSolidsCalculationAdmin)
