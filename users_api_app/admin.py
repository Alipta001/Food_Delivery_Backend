from django.contrib import admin
from .models import User, UserToken
# Register your models here.
if not admin.site.is_registered(User):
    admin.site.register(User)

if not admin.site.is_registered(UserToken):
    admin.site.register(UserToken)
    

 