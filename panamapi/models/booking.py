from django.db import models
from django.contrib.auth.models import User
from .payment import Payment


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    payment = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, null=True, related_name='bookings')  # null if not complete
    rewards_payment = models.BooleanField(null=True) #null if not complete/paid with dollars

