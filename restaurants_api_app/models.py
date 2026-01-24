from django.db import models
from django.core.validators import MaxValueValidator

class Restaurants(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    rating = models.FloatField()
    cuisine_type = models.CharField(max_length=100)
    image = models.ImageField(upload_to="restaurants/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Offer(models.Model):
    restaurant = models.OneToOneField(Restaurants, on_delete=models.CASCADE, related_name="offer")
    discount_percent = models.PositiveIntegerField(validators=[MaxValueValidator(100)])# 50
    max_discount = models.FloatField(null=True, blank=True)  # 100
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.discount_percent}% OFF at {self.restaurant.name}"
