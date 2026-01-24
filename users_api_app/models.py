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
    
class UserToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tokens')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_at = models.DateTimeField()

    def __str__(self):
        return f"Token for {self.user.email} expiring at {self.expiry_at}"
