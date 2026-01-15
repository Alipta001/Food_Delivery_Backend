from django.contrib import admin
from django.urls import path,include
from cart_api_app import views

urlpatterns = [
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('view/<int:user_id>/', views.view_cart, name='view_cart'),
    path('calculate-total/<int:user_id>/', views.calculate_cart_total, name='calculate_cart_total'),
    path('remove-item/', views.remove_item_from_cart, name='remove_item_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
]