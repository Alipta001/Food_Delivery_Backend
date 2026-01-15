from django.urls import path
from users_temp_app import views

urlpatterns = [
    path('register/', views.register_view, name='registerUser'),
]