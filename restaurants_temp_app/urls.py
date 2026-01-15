from django.urls import path,include
from restaurants_temp_app import views

urlpatterns = [
    path('',views.restaurent_list,name="restuarents"),
    path('add/',views.create_restaurent,name="add"),
    path('edit/<int:id>/',views.edit_restaurant,name="edit"),
    path('delete/<int:restaurant_id>/',views.delete_restaurant,name="delete")
]
