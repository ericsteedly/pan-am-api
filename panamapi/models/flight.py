from django.db import models
from .airport import Airport
import pytz
from datetime import datetime, timedelta


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
    
    
    # This property calculates the duration of a flight with airport timezones and cross-day flights considered.
    @property
    def duration(self):
        departure_tz = pytz.timezone(self.departureAirport.timezone)
        arrival_tz = pytz.timezone(self.arrivalAirport.timezone)
        departure_datetime = datetime.combine(self.departureDay, self.departureTime)
        departure_datetime = departure_tz.localize(departure_datetime, is_dst=None)
        arrival_datetime = datetime.combine(self.arrivalDay, self.arrivalTime)
        arrival_datetime = arrival_tz.localize(arrival_datetime, is_dst=None)

        if arrival_datetime < departure_datetime:
            arrival_datetime += timedelta(days=1)


        return arrival_datetime - departure_datetime