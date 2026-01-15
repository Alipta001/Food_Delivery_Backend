from django.urls import path
from menuItems_api_app import views

urlpatterns = [
    path('', views.create_menuItem, name='create_menuItem'),
    path('list_menuItems_api/', views.list_menuItems, name='list_menuItems'),
    path('patch_update_api/<int:pk>/', views.patch_menuItem, name='patch_update_menuItem'),
    path('full_update_api/', views.put_menuItem, name='full_update_menuItem'),
    path('delete_api/', views.delete_menuItem, name='delete_menuItem'),
    path('retrieve_api/<int:pk>/', views.retrieve_menuItem, name='retrieve_menuItem'),
    path('list_by_restaurant_api/<int:restaurant_id>/', views.list_menuItems_by_restaurant, name='list_menuItems_by_restaurant'),
    path('search_api/', views.search_menuItems, name='search_menuItems'),
]
