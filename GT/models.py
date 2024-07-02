from django.db import models

# Create your models here.
class Gt(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    more_info = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class aw_moisture(models.Model):
    min_moisture = models.FloatField()
    target_moisture = models.FloatField()
    max_moisture = models.FloatField()

class wb_moisture(models.Model):
    min_moisture = models.FloatField()
    target_moisture = models.FloatField()
    max_moisture = models.FloatField()
    
class ad_moisture(models.Model):
    min_moisture = models.FloatField()
    target_moisture = models.FloatField()
    max_moisture = models.FloatField()
    
class tg_moisture(models.Model):
    min_moisture = models.FloatField()
    target_moisture = models.FloatField()
    max_moisture = models.FloatField()