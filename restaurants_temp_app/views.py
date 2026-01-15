from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from restaurants_api_app.models import Restaurants
from django.db.models import QuerySet

def restaurent_list(request):
    restaurants: QuerySet = Restaurants.objects.all()
    return render(request, "restaurants/restaurants.html", {"restaurants": restaurants})


def create_restaurent(request):
    if request.method == "POST":

        restaurant_name: str = request.POST.get("restaurant_name")
        restaurant_address: str = request.POST.get("restaurant_address")
        cuisine_type: str = request.POST.get("cuisine_type")
        restaurant_rating: float = request.POST.get("restaurant_rating")
        image = request.FILES.get("image")

        if not all([restaurant_name, restaurant_address, cuisine_type, restaurant_rating]):
            return JsonResponse({"message": "All fields are required"}, status=400)

        if Restaurants.objects.filter(name=restaurant_name).exists():
            return JsonResponse({"message": "Restaurant already exists"}, status=400)

        Restaurants.objects.create(
            name=restaurant_name,
            address=restaurant_address,
            cuisine_type=cuisine_type,
            rating=restaurant_rating,
            image=image,
        )

        restaurants = Restaurants.objects.all()
        html = render_to_string("partial/restaurants_rows.html", {"restaurants": restaurants})

        return JsonResponse({"message": "Restaurant added successfully!", "restaurants": html}, status=201)

    return render(request, "restaurants/restaurants.html")


def edit_restaurant(request, id=None):
    if request.method == "POST":

        restaurant = Restaurants.objects.get(id=id)

        restaurant_name = request.POST.get("restaurant_name")
        restaurant_address = request.POST.get("restaurant_address")
        cuisine_type = request.POST.get("cuisine_type")
        restaurant_rating = request.POST.get("restaurant_rating")
        image = request.FILES.get("image")

        # Validate that all required fields are provided
        if not all([restaurant_name, restaurant_address, cuisine_type, restaurant_rating]):
            return JsonResponse({"message": "All fields are required"}, status=400)

        if Restaurants.objects.filter(name=restaurant_name).exclude(id=id).exists():
            return JsonResponse({"message": "Restaurant name already exists"}, status=400)

        restaurant.name = restaurant_name
        restaurant.address = restaurant_address
        restaurant.cuisine_type = cuisine_type
        restaurant.rating = restaurant_rating

        if image:
            restaurant.image = image

        restaurant.save()

        restaurants = Restaurants.objects.all()
        html = render_to_string("partial/restaurants_rows.html", {"restaurants": restaurants})

        return JsonResponse({"message": "Restaurant updated!", "restaurants": html}, status=200)

    return render(request, "restaurants/restaurants.html")


def delete_restaurant(request, restaurant_id):
    if request.method == "POST":
        restaurant = get_object_or_404(Restaurants, pk=restaurant_id)
        restaurant.delete()

        restaurants = Restaurants.objects.all()
        html = render_to_string("partial/restaurants_rows.html", {"restaurants": restaurants})

        return JsonResponse({"message": "Restaurant deleted!", "restaurants": html}, status=200)

    return render(request, "restaurants/restaurants.html")
