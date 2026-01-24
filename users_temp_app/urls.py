from django.urls import path
from users_temp_app import views

urlpatterns = [
    path('register/', views.register_view, name='registerUser'),
    path('login/', views.login_view, name='loginUser'),
    # path('dashboard/', views.dashboard_view, name='dashboard'),
    # path('logout/', views.logout_view, name='logoutUser'),
]






