from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404

from menuItems_api_app.models import MenuItem
from restaurants_api_app.models import Restaurants
from menuItems_api_app.serializers import MenuItemSerializer

@api_view(["POST"])
def create_menuItem(request: Request) -> Response:

    restaurant_id = request.data.get("restaurantId")
    name = request.data.get("itemName")
    description = request.data.get("description")
    price = request.data.get("price")
    image_file = request.FILES.get("imageURL")

    if not all([restaurant_id, name, description, price]):
        return Response({"error": "All fields except image are required"}, status=400)

    restaurant = get_object_or_404(Restaurants, pk=restaurant_id)

    if MenuItem.objects.filter(restaurant=restaurant, name=name).exists():
        return Response(
            {"error": "Menu Item already exists in this restaurant"},
            status=400
        )

    MenuItem.objects.create(
        restaurant=restaurant,
        name=name,
        description=description,
        price=price,
        imageURL=image_file
    )

    return Response(
        {"message": "Menu Item added successfully"},
        status=status.HTTP_201_CREATED
    )

@api_view(["GET"])
def list_menuItems(request: Request) -> Response:

    items = MenuItem.objects.select_related("restaurant")
    serializer = MenuItemSerializer(items, many=True)

    return Response(serializer.data, status=200)

@api_view(["PATCH"])
def patch_menuItem(request: Request, pk: int) -> Response:

    item = get_object_or_404(MenuItem, pk=pk)

    restaurant_id = request.data.get("restaurant", item.restaurant.id)
    name = request.data.get("name", item.name)

    restaurant = get_object_or_404(Restaurants, pk=restaurant_id)

    # Duplicate check: exclude itself
    if MenuItem.objects.filter(restaurant=restaurant, name=name).exclude(pk=pk).exists():
        return Response(
            {"error": "Another item with this name already exists in this restaurant"},status=status.HTTP_400_BAD_REQUEST)

    serializer = MenuItemSerializer(item, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)

    return Response(serializer.errors, status=400)

@api_view(["PUT"])
def put_menuItem(request: Request) -> Response:

    pk = request.data.get("id")
    if not pk:
        return Response({"error": "ID is required"}, status=400)

    item = get_object_or_404(MenuItem, pk=pk)

    restaurant_id = request.data.get("restaurant")
    if not restaurant_id:
        return Response({"restaurant": ["This field is required."]}, status=400)

    restaurant = get_object_or_404(Restaurants, pk=restaurant_id)

    # Duplicate check
    name = request.data.get("name", item.name)
    if MenuItem.objects.filter(restaurant=restaurant,name=name).exclude(pk=pk).exists():
        return Response(
            {"error": "Another item with this name already exists in this restaurant"},status=status.HTTP_400_BAD_REQUEST)

    serializer = MenuItemSerializer(item, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)

    return Response(serializer.errors, status=400)

@api_view(["DELETE"])
def delete_menuItem(request: Request) -> Response:

    pk = request.data.get("id")
    if not pk:
        return Response({"error": "ID is required"}, status=400)

    item = get_object_or_404(MenuItem, pk=pk)
    item.delete()

    return Response({"message": "Menu Item deleted successfully"}, status=200)

@api_view(["GET"])
def retrieve_menuItem(request: Request, pk: int) -> Response:

    item: MenuItem = get_object_or_404(MenuItem, pk=pk)
    serializer = MenuItemSerializer(item)

    return Response(serializer.data, status=200)

@api_view(["GET"])
def list_menuItems_by_restaurant(request: Request, restaurant_id: int) -> Response:
    restaurant = get_object_or_404(Restaurants, pk=restaurant_id)
    items = MenuItem.objects.filter(restaurant=restaurant)
    serializer = MenuItemSerializer(items, many=True)

    return Response(serializer.data, status=200)

@api_view(["GET"])
def search_menuItems(request: Request) -> Response:
    query = request.query_params.get("q", "").strip().lower()
    items = MenuItem.objects.filter(name__icontains=query)
    serializer = MenuItemSerializer(items, many=True)

    return Response(serializer.data, status=200)