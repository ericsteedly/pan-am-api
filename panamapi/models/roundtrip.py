from django.db import models
from .booking import Booking

class RoundTrip(models.Model):
    departure_booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="departure_booking")
    return_booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="return_booking")