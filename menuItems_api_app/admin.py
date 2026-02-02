from django.contrib import admin
from .models import MenuItem,MenuItemImage

# Register your models here.
if not admin.site.is_registered(MenuItem):
    admin.site.register(MenuItem)
if not admin.site.is_registered(MenuItemImage):
    admin.site.register(MenuItemImage)
