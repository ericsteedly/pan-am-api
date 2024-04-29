from django.db import models
from django.contrib.auth.models import User
from .flight import Flight
from .booking import Booking

class Ticket(models.Model):
    id = models.IntegerField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='tickets')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tickets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')