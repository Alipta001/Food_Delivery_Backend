from django.db import models
from restaurants_api_app.models import Restaurants

# Create your models here.
class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE,related_name='menu_items')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    imageURL = models.ImageField(upload_to='menu_items/', null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name