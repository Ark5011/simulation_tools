from django.db import models

class InputData(models.Model):
    primaryairAH = models.FloatField(default=0.0)
    primaryair = models.FloatField(default=0.0)
    primaryinletT = models.FloatField(default=0.0)
    outletairT = models.FloatField(default=0.0)
    sfbair = models.FloatField(default=0.0)
    sfbinletT = models.FloatField(default=0.0)
    roofcoolingair = models.FloatField(default=0.0)
    roofcoolingT = models.FloatField(default=0.0)
    temperature = models.FloatField(default=0.0)
    altitude = models.FloatField(default=0.0)
    totalsolids = models.FloatField(default=0.0)
    moisture = models.FloatField(default=0.0)
    sfbinletAH = models.FloatField(default=0.0)

    def __str__(self):
        return f"Input Data {self.id}"


class CalculatedData(models.Model):
    input_data = models.OneToOneField(InputData, on_delete=models.CASCADE)
    sfb_inlet_rh = models.FloatField()
    outlet_air_ah = models.FloatField()
    outlet_air_rh = models.FloatField()
    dummy_outlet_air_rh = models.FloatField()
    dummy_outlet_air_t = models.FloatField()
    production_rate = models.FloatField()
    barometric_pressure = models.FloatField()

    def __str__(self):
        return f"Calculated Data {self.id}"
