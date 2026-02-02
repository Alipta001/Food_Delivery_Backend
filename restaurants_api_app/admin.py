from django.contrib import admin
from .models import Restaurants,RestaurantImage,Offer
# Register your models here.
if not admin.site.is_registered(Restaurants):
    admin.site.register(Restaurants)

if not admin.site.is_registered(RestaurantImage):
    admin.site.register(RestaurantImage)

if not admin.site.is_registered(Offer):
    admin.site.register(Offer)