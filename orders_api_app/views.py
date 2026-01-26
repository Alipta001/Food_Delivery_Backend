from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from cart_api_app.models import Cart
from .models import Order, OrderItem
from users_api_app.models import User
from .serializers import OrderSerializer

@api_view(['POST'])
def place_order(request):
    user_id = request.data.get('user_id')

    if not user_id:
        return Response({"error": "user_id is required"}, status=400)

    try:
        user = User.objects.get(id=user_id)
        cart = Cart.objects.get(user=user)
    except (User.DoesNotExist, Cart.DoesNotExist):
        return Response({"error": "User or Cart not found"}, status=404)

    cart_items = cart.cart_items.select_related("menu_item", "menu_item__restaurant")

    if not cart_items.exists():
        return Response({"error": "Cart is empty"}, status=400)

    restaurant = cart_items.first().menu_item.restaurant
    total_amount = 0

    order = Order.objects.create(user=user,restaurant=restaurant,totalAmount=0)
    
    for item in cart_items:
        price = item.menu_item.price
        total_amount += price * item.quantity

        OrderItem.objects.create(
            order=order,
            menu_item=item.menu_item,
            quantity=item.quantity,
            price=price
        )

    order.totalAmount = total_amount
    order.save()

    # Clear cart
    cart.cart_items.all().delete()

    return Response(
        {"message": "Order placed successfully", "order_id": order.id},
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
def track_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['PATCH'])
def update_order_status(request, order_id):
    status_value = request.data.get("status")

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    order.status = status_value
    order.save()

    return Response({"message": "Order status updated"})

