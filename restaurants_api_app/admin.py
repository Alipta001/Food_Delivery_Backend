from django.contrib import admin
from .models import Restaurants
# Register your models here.
if not admin.site.is_registered(Restaurants):
    admin.site.register(Restaurants)