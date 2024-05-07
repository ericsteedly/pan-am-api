from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    merchant = models.CharField(max_length=25)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    number = models.CharField(max_length=25)
    expDate = models.DateField()
    CVV = models.IntegerField(validators=[MaxLengthValidator(4)])