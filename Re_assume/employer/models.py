from django.db import models
from django.db.models.signals import *
from django.core.validators import RegexValidator
from django.utils.timesince import timesince
from django.utils.timezone import is_aware, make_aware, get_current_timezone
from datetime import datetime
class employer_table(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_no = models.CharField(
        max_length=10, 
        unique=True, 
        validators=[RegexValidator(r'^\d{10}$', 'Phone number must be a 10-digit number.')],
        null=True
    )
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Store hashed passwords
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    age = models.CharField(max_length=10, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    company_exist = models.BooleanField(default=False)
    def __str__(self):
        return self.email
 