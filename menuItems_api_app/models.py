from django.db import models
from restaurants_api_app.models import Restaurants

class MenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurants,
        on_delete=models.CASCADE,
        related_name="menu_items"
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MenuItemImage(models.Model):
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="menu_items/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.menu_item.name}"
