from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import RestaurantSerializer
from django.shortcuts import render, get_object_or_404
from django.db.models import QuerySet
from .models import Restaurants, Offer, RestaurantImage
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
# Create your views here.

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def create_api(request: Request) -> Response:
    name = request.data.get("name")
    address = request.data.get("address")
    rating = request.data.get("rating")
    cuisine_type = request.data.get("cuisine_type")

    images = request.FILES.getlist("images")  # 🔥 ARRAY

    if not all([name, address, rating, cuisine_type]):
        return Response(
            {"error": "All fields are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if Restaurants.objects.filter(name=name).exists():
        return Response(
            {"error": "Restaurant already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    restaurant = Restaurants.objects.create(
        name=name.capitalize(),
        address=address,
        rating=float(rating),
        cuisine_type=cuisine_type,
    )

    # 🔥 Save multiple images
    for img in images:
        RestaurantImage.objects.create(
            restaurant=restaurant,
            image=img
        )

    serializer = RestaurantSerializer(restaurant)

    return Response(
        {
            "message": "Restaurant created successfully",
            "data": serializer.data
        },
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
def display_api(request):
    restaurants = Restaurants.objects.all()
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['PATCH'])
# @permission_classes([IsAuthenticated])
def update_patch_api(request, pk):
    try:
        restaurant = Restaurants.objects.get(pk=pk)
    except Restaurants.DoesNotExist:
        return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check for name uniqueness if name is being updated
    new_name = request.data.get("name")
    if new_name:
        if Restaurants.objects.filter(name=new_name).exclude(pk=pk).exists():
            return Response({"error": "Restaurant name already exists"},
                            status=status.HTTP_400_BAD_REQUEST)

    serializer = RestaurantSerializer(restaurant, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
def update_put_api(request):
    pk = request.data.get("id")
    if not pk:
        return Response(
            {"error": "Restaurant ID is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        restaurant = Restaurants.objects.get(pk=pk)
    except Restaurants.DoesNotExist:
        return Response(
            {"error": "Restaurant not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # ---------- Update normal fields ----------
    serializer = RestaurantSerializer(
        restaurant,
        data=request.data,
        partial=True
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    serializer.save()

    # ---------- Handle images (optional) ----------
    images = request.FILES.getlist("images")

    if images:
        # Delete old images
        restaurant.images.all().delete()

        # Add new images
        for img in images:
            RestaurantImage.objects.create(
                restaurant=restaurant,
                image=img
            )

    return Response(
        {
            "message": "Restaurant updated successfully",
            "data": RestaurantSerializer(restaurant).data
        },
        status=status.HTTP_200_OK
    )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_api(request):
    pk = request.data.get("id")

    if not pk:
        return Response({"error": "ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        restaurant = Restaurants.objects.get(pk=pk)
        restaurant.delete()
        return Response({"message": "Restaurant deleted successfully"},
                        status=status.HTTP_200_OK)
    except Restaurants.DoesNotExist:
        return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def get_restaurant_by_id(request:Request, pk: int) -> Response:
    try:
        restaurant = Restaurants.objects.get(pk=pk)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Restaurants.DoesNotExist:
        return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def search_restaurents(request: Request) -> Response:
    query: str = request.query_params.get("q", "").strip()
    if not query:
        return Response(
            {"error": "Search query parameter 'q' is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    restaurants: QuerySet = Restaurants.objects.filter(name__icontains=query) | Restaurants.objects.filter(cuisine_type__icontains=query)

    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_or_update_offer(request, restaurant_id):
    restaurant = get_object_or_404(Restaurants, pk=restaurant_id)

    discount_percent = request.data.get("discount_percent")
    max_discount = request.data.get("max_discount")

    if not discount_percent:
        return Response({"error": "discount_percent required"}, status=400)

    offer, created = Offer.objects.update_or_create(
        restaurant=restaurant,
        defaults={
            "discount_percent": discount_percent,
            "max_discount": max_discount,
            "is_active": True
        }
    )

    return Response(
        {"message": "Offer applied successfully"},
        status=status.HTTP_200_OK
    )
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def disable_offer(request, restaurant_id):
    restaurant = get_object_or_404(Restaurants, pk=restaurant_id)

    if hasattr(restaurant, "offer"):
        restaurant.offer.is_active = False
        restaurant.offer.save()

    return Response({"message": "Offer disabled"}, status=200)
