from rest_framework import serializers
from .models import Cart, CartItem
from menuItems_api_app.serializers import MenuItemSerializer

class CartItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = "__all__"
    
class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"
        

class AddToCartSerializer(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)


