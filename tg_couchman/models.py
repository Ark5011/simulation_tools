from django.db import models

class Tg(models.Model):
    water = models.FloatField()
    casein = models.FloatField()
    whey_protein = models.FloatField()
    lactose = models.FloatField()
    GOS = models.FloatField()
    PDX = models.FloatField()

    # def __str__(self):
    #     return self.title

class Final_Tg(models.Model):
    final_tg_min = models.FloatField()
    final_tg_target = models.FloatField()
    final_tg_max = models.FloatField()

class Cp(models.Model):
    water = models.FloatField()
    casein = models.FloatField()
    whey_protein = models.FloatField()
    lactose = models.FloatField()
    GOS = models.FloatField()
    PDX = models.FloatField()
    
class Formulation(models.Model):
    water_min = models.FloatField()
    casein = models.FloatField()
    whey_protein = models.FloatField()
    lactose = models.FloatField()
    GOS = models.FloatField()
    PDX = models.FloatField()
    
    # @property
    # def lactose(self):
    #     lactose = 50.9 - self.GOS + self.PDX
    #     return lactose
