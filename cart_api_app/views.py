from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import CartSerializer, AddToCartSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import Cart, CartItem
from menuItems_api_app.models import MenuItem
from users_api_app.models import User
# Create your views here.
@api_view(['POST'])
def add_to_cart(request):
    menu_item_id = request.data.get('menu_item_id')
    quantity = request.data.get('quantity', 1)
    user_id = request.data.get('user_id')

    
    if not user_id and not menu_item_id:
        return Response(
            {"error": "user_id and menu_item_id are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError
    except ValueError:
        return Response(
            {"error": "quantity must be a positive integer"},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    try:
        menu_item = MenuItem.objects.get(id=menu_item_id)
    except MenuItem.DoesNotExist:
        return Response(
            {"error": "Menu item not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # One user → one cart
    cart, _ = Cart.objects.get_or_create(user=user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        menu_item=menu_item
    )

    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    cart_item.save()

    return Response(
        {
            "message": "Item added to cart successfully",
            "cart": {
                "id": cart.id,
                "user": cart.user.id,
                "items": [
                    {
                        "menu_item_id": cart_item.menu_item.id,
                        "menu_item_name": cart_item.menu_item.name,
                        "price": cart_item.menu_item.price,
                        "quantity": cart_item.quantity
                    }
                ]
            }
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def view_cart(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return Response(
            {"error": "Cart not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def calculate_cart_total(request, user_id):
    try:
        user: User = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )
        
    try:
        cart: Cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return Response(
            {"error": "Cart not found"},
            status=status.HTTP_404_NOT_FOUND
        )
        
    total_amount = 0
    items_data = []

    for item in cart.cart_items.all():
        item_total = item.menu_item.price * item.quantity
        total_amount += item_total

        items_data.append({
            "menu_item_id": item.menu_item.id,
            "menu_item_name": item.menu_item.name,
            "price": item.menu_item.price,
            "quantity": item.quantity,
            "item_total": item_total
        })

    return Response(
        {
            "user_id": user.id,
            "cart_id": cart.id,
            "items": items_data,
            "total_amount": total_amount
        },
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
def remove_item_from_cart(request):
    user_id = request.data.get('user_id')
    menu_item_id = request.data.get('menu_item_id')

    if not user_id or not menu_item_id:
        return Response(
            {"error": "user_id and menu_item_id are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return Response(
            {"error": "Cart not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        cart_item = CartItem.objects.get(
            cart=cart,
            menu_item_id=menu_item_id
        )
    except CartItem.DoesNotExist:
        return Response(
            {"error": "Item not found in cart"},
            status=status.HTTP_404_NOT_FOUND
        )

    cart_item.delete()

    return Response(
        {"message": "Item removed from cart successfully"},
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
def clear_cart(request):
    user_id = request.data.get('user_id')

    if not user_id:
        return Response(
            {"error": "user_id is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return Response(
            {"error": "Cart not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    cart.cart_items.all().delete()

    return Response(
        {"message": "Cart cleared successfully"},
        status=status.HTTP_200_OK
    )
