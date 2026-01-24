from rest_framework import serializers
from .models import Restaurants

class RestaurantSerializer(serializers.ModelSerializer):
    offer = serializers.SerializerMethodField()

    class Meta:
        model = Restaurants
        fields = "__all__"

    def get_offer(self, obj):
        if hasattr(obj, "offer") and obj.offer.is_active:
            return {
                "id": obj.offer.id,
                "discount_percent": obj.offer.discount_percent,
                "max_discount": obj.offer.max_discount
            }
        return None
