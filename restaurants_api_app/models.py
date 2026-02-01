from django.db import models
from django.core.validators import MaxValueValidator


class Restaurants(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    rating = models.FloatField()
    cuisine_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(
        Restaurants,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="restaurants/")

    def __str__(self):
        return f"Image for {self.restaurant.name}"


class Offer(models.Model):
    restaurant = models.OneToOneField(
        Restaurants,
        on_delete=models.CASCADE,
        related_name="offer"
    )
    discount_percent = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)]
    )
    max_discount = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.discount_percent}% OFF at {self.restaurant.name}"
