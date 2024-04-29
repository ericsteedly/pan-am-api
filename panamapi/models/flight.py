from django.db import models
from .airport import Airport


class Flight(models.Model):
    id = models.IntegerField(primary_key=True)
    departureAirport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure_flights')
    departureDay = models.DateField()
    departureTime = models.TimeField()
    arrivalAirport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrival_flights')
    arrivalDay = models.DateField()
    arrivalTime = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    points = models.IntegerField()
    seats = models.IntegerField()