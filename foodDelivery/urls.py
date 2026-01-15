from django.contrib import admin
from django.urls import path,include
from foodDelivery import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('restaurants-temp/',include('restaurants_temp_app.urls')),
    path('restaurants-api/',include('restaurants_api_app.urls')),
    path('menuItems-temp/',include('menuItems_temp_app.urls')),
    path('menuItems-api/',include('menuItems_api_app.urls')),
    path('cart-api/',include('cart_api_app.urls')),
    path('users-temp/',include('users_temp_app.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
