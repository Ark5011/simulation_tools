from django.db import models

class NozzleCalculation(models.Model):
    num_nozzles = models.FloatField()
    swirl_number = models.CharField(max_length=50)
    orifice_number = models.FloatField()
    operating_pressure = models.FloatField()
    lsg = models.FloatField()
    lpcs = models.FloatField()
    ppcm = models.FloatField()

    def __str__(self):
        return f"Nozzle Calculation {self.id} - Swirl Number: {self.swirl_number}"

class NozzleTDResult(models.Model):
    calculation = models.ForeignKey(NozzleCalculation, on_delete=models.CASCADE)
    liquid_flow_rate = models.FloatField()
    spray_angle = models.FloatField()
    droplet_size = models.FloatField()
    powder_flow_rate = models.FloatField()

    def __str__(self):
        return f"Nozzle TD Result {self.id} - Calculation: {self.calculation.id}"

class NozzleTDLResult(models.Model):
    calculation = models.ForeignKey(NozzleCalculation, on_delete=models.CASCADE)
    liquid_flow_rate = models.FloatField()
    powder_flow_rate = models.FloatField()

    def __str__(self):
        return f"Nozzle TDL Result {self.id} - Calculation: {self.calculation.id}"