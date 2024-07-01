from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    more_info = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Tg(models.Model):
    water = models.FloatField()
    casein = models.FloatField()
    whey_protein = models.FloatField()
    lactose = models.FloatField()
    GOS = models.FloatField()
    PDX = models.FloatField()

    # def __str__(self):
    #     return self.title

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
    GOS = models.FloatField()
    PDX = models.FloatField()
    
    # @property
    # def lactose(self):
    #     lactose = 50.9 - self.GOS + self.PDX
    #     return lactose
