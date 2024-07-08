from django.db import models

# Create your models here.
class Gt_input(models.Model):
    aw_min = models.FloatField()
    aw_target = models.FloatField()
    aw_max = models.FloatField()
    aw_actual = models.FloatField()
    aw_sample = models.FloatField()
    w_actual = models.FloatField()
    w_sample = models.FloatField()
    tg_actual = models.FloatField()
    tg_sample = models.FloatField()
    spraydry_min = models.FloatField()
    spraydry_target = models.FloatField()
    spraydry_max = models.FloatField()
    sfb_min = models.FloatField()
    sfb_target = models.FloatField()
    sfb_max = models.FloatField()
    tg_dry = models.FloatField()
    k = models.FloatField()
