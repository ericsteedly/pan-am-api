from django.db import models
from django.core.validators import MaxLengthValidator, RegexValidator
from django.contrib.auth.models import User

exp_date_pattern = r'^(0[1-9]|1[0-2])/\d{2}$'

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    merchant = models.CharField(max_length=25)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=25)
    expiration_date = models.CharField(max_length=5, validators=[RegexValidator(exp_date_pattern, 'Invalid expiration date format. Use MM/YY.')])
    CVV = models.IntegerField(validators=[MaxLengthValidator(4)])


    @property
    def obscured_num(self):
        # Replaces all but the last 3 digits with asterisks
        if self.card_number is not None:
            obscured_digits = "*" * (len(self.card_number) - 3)
            visible_digits = self.card_number[-3:]
            return obscured_digits + visible_digits
        else:
            return None