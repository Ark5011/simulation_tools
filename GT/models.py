from django.db import models

# Create your models here.
class Gt(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    more_info = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Graph_w(models.Model):
    W = models.FloatField()

class Graph_tg(models.Model):
    Tg = models.FloatField()