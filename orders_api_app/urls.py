from django.urls import path
from .views import place_order, track_order, update_order_status

urlpatterns = [
    path("place-order/", place_order),
    path("track-order/<int:order_id>/", track_order),
    path("/<int:order_id>/", update_order_status),
]
