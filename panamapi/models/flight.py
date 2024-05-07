from django.db import models
from .airport import Airport
import pytz
from datetime import datetime


class Flight(models.Model):
    departureAirport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure_flights')
    departureDay = models.DateField()
    departureTime = models.TimeField()
    arrivalAirport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrival_flights')
    arrivalDay = models.DateField()
    arrivalTime = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    points = models.IntegerField()
    seats = models.IntegerField()

    @property
    def duration(self):
        departure_tz = pytz.timezone(self.departureAirport.timezone)
        arrival_tz = pytz.timezone(self.arrivalAirport.timezone)
        departure_datetime = departure_tz.localize(
            datetime.combine(self.departureDay, self.departureTime)
        )
        arrival_datetime = arrival_tz.localize(
            datetime.combine(self.arrivalDay, self.arrivalTime)
        )

        return(arrival_datetime - departure_datetime)