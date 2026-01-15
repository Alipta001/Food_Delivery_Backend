from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import RestaurantSerializer
from django.shortcuts import render
from django.db.models import QuerySet
from .models import Restaurants
# Create your views here.
@api_view(['POST'])
def create_api(request: Request) -> Response:
    try:
        name: str = request.data.get("name")
        if name:
            name = name.capitalize()
        address: str = request.data.get("address")
        rating: str = request.data.get("rating")
        cuisine_type: str = request.data.get("cuisine_type")
        image = request.FILES.get("image")

        # Validate rating
        try:
            rating = float(rating) if rating else None
        except (ValueError, TypeError):
            return Response(
                {"error": "Rating must be a valid number."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not all([name, address, rating, cuisine_type, image]):
            return Response(
                {"error": "All fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not Restaurants.objects.filter(name=name).exists():
            Restaurants.objects.create(
                name=name,
                address=address,
                rating=rating,
                cuisine_type=cuisine_type,
                image=image
            )
            response_data = {
                "message": "Restaurant created successfully!",
                "restaurant": {
                    "name": name,
                    "address": address,
                    "rating": rating,
                    "cuisine_type": cuisine_type,
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(
            {"error": "Restaurant with this name already exists."},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": f"An error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def display_api(request):
    restaurants = Restaurants.objects.all()
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
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

@api_view(['PUT'])
def update_put_api(request):
    pk = request.data.get("id")
    if not pk:
        return Response({"error": "ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        restaurant = Restaurants.objects.get(pk=pk)
    except Restaurants.DoesNotExist:
        return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = RestaurantSerializer(restaurant, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
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