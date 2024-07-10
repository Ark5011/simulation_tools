from django.db import models

class TotalSolidsCalculation(models.Model):
    fat_content = models.FloatField()
    start_density = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class TotalSolidsResult(models.Model):
    calculation = models.ForeignKey(TotalSolidsCalculation, related_name='results', on_delete=models.CASCADE)
    iteration = models.IntegerField()
    density = models.FloatField()
    total_solids = models.FloatField()
