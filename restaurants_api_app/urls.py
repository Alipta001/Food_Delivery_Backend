from django.urls import path
from .views import create_api,display_api,update_patch_api,update_put_api,delete_api, get_restaurant_by_id,search_restaurents

urlpatterns = [
    path('',create_api,name="add_restuarents"),
    path("restuarents_list/", display_api,name="restuarents_list"),
    path('update_patch_api/<int:pk>/', update_patch_api, name='update_api'),
    path('update_put_api/',update_put_api,name="update_put_api"),
    path('delete_api/',delete_api,name="delete_api"),
    path('get_restaurant/<int:pk>/', get_restaurant_by_id, name='get_restaurant_by_id'),
    path('search/', search_restaurents, name='search_restaurants'),
]