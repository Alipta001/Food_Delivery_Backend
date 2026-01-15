from django.db import models

# Create your models here.
from django.db import models
from users_api_app.models import User
from restaurants_api_app.models import Restaurants
from menuItems_api_app.models import MenuItem

ORDER_STATUS = [
    ('Pending', 'Pending'),
    ('Preparing', 'Preparing'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Delivered', 'Delivered'),
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
    items = models.JSONField()
    totalAmount = models.FloatField()
    status = models.CharField(max_length=50, choices=ORDER_STATUS, default="Pending")
    createdAt = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()
