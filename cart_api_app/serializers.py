# from rest_framework import serializers
# from .models import Cart, CartItem
# from menuItems_api_app.serializers import MenuItemSerializer

# class CartItemSerializer(serializers.ModelSerializer):
#     menu_item = MenuItemSerializer(read_only=True)
#     class Meta:
#         model = CartItem
#         fields = "__all__"
    
# class CartSerializer(serializers.ModelSerializer):
#     cart_items = CartItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = Cart
#         fields = "__all__"
        

# class AddToCartSerializer(serializers.Serializer):
#     menu_item_id = serializers.IntegerField()
#     quantity = serializers.IntegerField(default=1)


from rest_framework import serializers
from .models import Cart, CartItem
from menuItems_api_app.serializers import MenuItemSerializer


class CartItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "menu_item",
            "quantity",
            "price",
            "item_total"
        ]

    def get_item_total(self, obj):
        return round(obj.price * obj.quantity, 2)


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "cart_items",
            "total_amount",
            "created_at",
            "updated_at"
        ]

    def get_total_amount(self, obj):
        return round(obj.total_amount(), 2)


class AddToCartSerializer(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)
