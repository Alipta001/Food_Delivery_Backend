from django.contrib import admin

# Register your models here.

from .models import Order, OrderItem

if not admin.site.is_registered(Order):
    admin.site.register(Order)
if not admin.site.is_registered(OrderItem):
    admin.site.register(OrderItem)
