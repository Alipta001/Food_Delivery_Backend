from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # Role constants
    ADMIN = 'admin'
    CUSTOMER = 'customer'
    DELIVERY_PERSON = 'delivery_person'

    # Role choices
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (CUSTOMER, 'Customer'),
        (DELIVERY_PERSON, 'Delivery Person'),
    ]
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email
