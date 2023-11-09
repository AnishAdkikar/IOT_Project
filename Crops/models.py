from django.db import models

# Create your models here.


class Wheat(models.Model):
    Date_of_harvest = models.DateField()
    Uid = models.TextField()
    Section = models.IntegerField()
    Temp = models.FloatField()
    Pressure = models.FloatField()
    Weight = models.FloatField()
    CO2 = models.FloatField()
    Price = models.FloatField(null=True, blank=True)
    Est_date_of_exp = models.DateField()
