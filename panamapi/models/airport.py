from django.db import models

class Airport(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    airport_code = models.CharField(max_length=3)
    timezone = models.CharField(max_length=64, default='UTC')