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


    @property
    def obscured_num(self):
        # Replaces all but the last 3 digits with asterisks
        if self.account_number is not None:
            obscured_digits = "*" * (len(self.account_number) - 3)
            visible_digits = self.account_number[-3:]
            return obscured_digits + visible_digits
        else:
            return None