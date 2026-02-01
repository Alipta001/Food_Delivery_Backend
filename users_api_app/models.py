from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    ADMIN = 'admin'
    CUSTOMER = 'customer'
    DELIVERY_PERSON = 'delivery_person'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (CUSTOMER, 'Customer'),
        (DELIVERY_PERSON, 'Delivery Person'),
    ]

    username = models.CharField(
        max_length=255,
        blank=False
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class UserToken(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tokens'
    )
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_at = models.DateTimeField()

    def __str__(self):
        return f"Token for {self.user.email} expiring at {self.expiry_at}"


class LoginOTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"OTP for {self.user.email}"
