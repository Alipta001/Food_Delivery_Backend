from rest_framework import serializers
from menuItems_api_app.models import MenuItem, MenuItemImage

class MenuItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemImage
        fields = ["id", "image"]


class MenuItemSerializer(serializers.ModelSerializer):
    images = MenuItemImageSerializer(many=True, read_only=True)
    discounted_price = serializers.SerializerMethodField()
    offer_text = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = "__all__"

    def get_discounted_price(self, obj):
        restaurant = obj.restaurant

        if hasattr(restaurant, "offer") and restaurant.offer.is_active:
            offer = restaurant.offer
            discount = (offer.discount_percent / 100) * obj.price

            if offer.max_discount:
                discount = min(discount, offer.max_discount)

            return round(max(obj.price - discount, 0), 2)

        return obj.price

    def get_offer_text(self, obj):
        restaurant = obj.restaurant
        if hasattr(restaurant, "offer") and restaurant.offer.is_active:
            return f"{restaurant.offer.discount_percent}% OFF"
        return None
