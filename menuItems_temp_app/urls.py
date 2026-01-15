from django.urls import path
from menuItems_temp_app import views

urlpatterns = [
    path('', views.list_menuItems, name='menuItems'),
    path('add/', views.create_menuItem, name='add_menuItem'),
    path('edit/<int:id>/', views.edit_menuItem, name='edit_menuItem'),
    path('delete/<int:id>/', views.delete_menuItem, name='delete_menuItem'),
]