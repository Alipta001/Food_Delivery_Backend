from django.contrib import admin
from .models import MenuItem

# Register your models here.
if not admin.site.is_registered(MenuItem):
    admin.site.register(MenuItem)
