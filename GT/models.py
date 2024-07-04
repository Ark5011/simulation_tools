from django.db import models

# Create your models here.
class Gt_input(models.Model):
    aw_1 = models.FloatField()
    aw_2 = models.FloatField()
    aw_3 = models.FloatField()
    aw_4 = models.FloatField()
    aw_5 = models.FloatField()
    wb_1 = models.FloatField()
    wb_2 = models.FloatField()
    wb_3 = models.FloatField()
    wb_4 = models.FloatField()
    wb_5 = models.FloatField()
    

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