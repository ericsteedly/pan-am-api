from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING,)
    date_of_birth = models.DateField()
    phone_number = models.IntegerField(validators=[MaxLengthValidator(15)])