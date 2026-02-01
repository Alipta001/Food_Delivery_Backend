from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from menuItems_api_app.models import MenuItem, MenuItemImage
from restaurants_api_app.models import Restaurants
from menuItems_api_app.serializers import MenuItemSerializer


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def create_menuItem(request: Request) -> Response:

    restaurant_id = request.data.get("restaurantId")
    name = request.data.get("itemName")
    description = request.data.get("description")
    price = request.data.get("price")
    images = request.FILES.getlist("images")

    if not all([restaurant_id, name, description, price]):
        return Response(
            {"error": "restaurant, name, description and price are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    restaurant = get_object_or_404(Restaurants, pk=restaurant_id)

    if MenuItem.objects.filter(restaurant=restaurant, name=name).exists():
        return Response(
            {"error": "Menu item already exists in this restaurant"},
            status=status.HTTP_400_BAD_REQUEST
        )

    menu_item = MenuItem.objects.create(
        restaurant=restaurant,
        name=name,
        description=description,
        price=price
    )

    for img in images:
        MenuItemImage.objects.create(
            menu_item=menu_item,
            image=img
        )

    serializer = MenuItemSerializer(menu_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_menuItems(request: Request) -> Response:

    items = MenuItem.objects.select_related(
        "restaurant", "restaurant__offer"
    ).prefetch_related("images")

    serializer = MenuItemSerializer(items, many=True)
    return Response(serializer.data, status=200)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def patch_menuItem(request: Request, pk: int) -> Response:

    item = get_object_or_404(MenuItem, pk=pk)

    restaurant_id = request.data.get("restaurant", item.restaurant.id)
    name = request.data.get("name", item.name)

    restaurant = get_object_or_404(Restaurants, pk=restaurant_id)

    if MenuItem.objects.filter(
        restaurant=restaurant, name=name
    ).exclude(pk=pk).exists():
        return Response(
            {"error": "Another item with this name exists in this restaurant"},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = MenuItemSerializer(item, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

        images = request.FILES.getlist("images")
        for img in images:
            MenuItemImage.objects.create(menu_item=item, image=img)

        return Response(serializer.data, status=200)

    return Response(serializer.errors, status=400)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def put_menuItem(request: Request) -> Response:

    pk = request.data.get("id")
    if not pk:
        return Response({"error": "ID is required"}, status=400)

    item = get_object_or_404(MenuItem, pk=pk)

    restaurant_id = request.data.get("restaurant")
    if not restaurant_id:
        return Response({"restaurant": ["This field is required"]}, status=400)

    restaurant = get_object_or_404(Restaurants, pk=restaurant_id)

    name = request.data.get("name")
    if MenuItem.objects.filter(
        restaurant=restaurant, name=name
    ).exclude(pk=pk).exists():
        return Response(
            {"error": "Another item with this name exists in this restaurant"},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = MenuItemSerializer(item, data=request.data)

    if serializer.is_valid():
        serializer.save()

        images = request.FILES.getlist("images")
        if images:
            item.images.all().delete()
            for img in images:
                MenuItemImage.objects.create(menu_item=item, image=img)

        return Response(serializer.data, status=200)

    return Response(serializer.errors, status=400)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_menuItem(request: Request) -> Response:

    pk = request.data.get("id")
    if not pk:
        return Response({"error": "ID is required"}, status=400)

    item = get_object_or_404(MenuItem, pk=pk)
    item.delete()

    return Response({"message": "Menu item deleted successfully"}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_menuItem(request: Request, pk: int) -> Response:

    item = get_object_or_404(
        MenuItem.objects.prefetch_related("images"),
        pk=pk
    )

    serializer = MenuItemSerializer(item)
    return Response(serializer.data, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_menuItems_by_restaurant(request: Request, restaurant_id: int) -> Response:

    restaurant = get_object_or_404(Restaurants, pk=restaurant_id)
    items = MenuItem.objects.filter(
        restaurant=restaurant
    ).prefetch_related("images")

    serializer = MenuItemSerializer(items, many=True)
    return Response(serializer.data, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_menuItems(request: Request) -> Response:

    query = request.query_params.get("q", "").strip()
    items = MenuItem.objects.filter(
        name__icontains=query
    ).prefetch_related("images")

    serializer = MenuItemSerializer(items, many=True)
    return Response(serializer.data, status=200)
