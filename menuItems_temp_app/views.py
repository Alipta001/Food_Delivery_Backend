from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from menuItems_api_app.models import MenuItem
from restaurants_api_app.models import Restaurants
from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status

# Create your views here.
def list_menuItems(request:HttpRequest)-> HttpResponse:
    if request.method == 'GET':
        menuItems: QuerySet = MenuItem.objects.all()
        restaurants: QuerySet = Restaurants.objects.all()
        return render(request, 'menuItems/menuItems.html', {'menuItems': menuItems, 'restaurants': restaurants})
       
def create_menuItem(request):
    if request.method == "POST":
        restaurant_id = int(request.POST.get("restaurant_id"))
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = float(request.POST.get("price"))
        image_file = request.FILES.get("image")
    
        print(f"restaurant_id={restaurant_id}, name={name}, description={description}, price={price}, image={image_file}")

        if not all([restaurant_id, name, description, price, image_file]):
            return JsonResponse({"message": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            restaurant: Restaurants = Restaurants.objects.get(id=restaurant_id)
            print(f"Found restaurant: {restaurant}")
        except Restaurants.DoesNotExist:
            return JsonResponse({"message": "Restaurant not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Check for duplicate menu item name within the same restaurant
        if MenuItem.objects.filter(name=name, restaurant=restaurant).exists():
            return JsonResponse({"message": "Item with this name already exists for this restaurant"}, status=status.HTTP_400_BAD_REQUEST)
        
        MenuItem.objects.create(restaurant=restaurant, name=name, description=description, price=price, imageURL=image_file)

        menuItems: QuerySet = MenuItem.objects.select_related("restaurant")

        html_string: str = render_to_string("partial/menuItems_row.html", {"menuItems": menuItems})
        return JsonResponse({"menuItems": html_string, "message": "Menu item added successfully"}, status=status.HTTP_201_CREATED)

def edit_menuItem(request: HttpRequest, id: int)-> HttpResponse:
    if request.method == "POST":
        restaurant_id = int(request.POST.get("restaurant_id"))
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = float(request.POST.get("price"))
        image_file = request.FILES.get("image")

        if not all([restaurant_id, name, description, price]):
            return JsonResponse({"message": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            restaurant: Restaurants = get_object_or_404(Restaurants, id=restaurant_id)
        except Restaurants.DoesNotExist:
            return JsonResponse({"message": "Restaurant not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            menu_item: MenuItem = get_object_or_404(MenuItem, pk=id)
        except MenuItem.DoesNotExist:
            return JsonResponse({"message": "Menu item not found"}, status=status.HTTP_400_BAD_REQUEST)

        if not MenuItem.objects.filter(name=name, restaurant=restaurant).exclude(id=menu_item.id).exists():
            menu_item.restaurant = restaurant
            menu_item.name = name
            menu_item.description = description
            menu_item.price = price
            if image_file:
                menu_item.imageURL = image_file
            menu_item.save()
            menuItems: QuerySet = MenuItem.objects.select_related("restaurant")
            html_string: str = render_to_string("partial/menuItems_row.html", {"menuItems": menuItems})
            return JsonResponse({"menuItems": html_string, "message": "Menu item updated successfully"}, status=200)
            
        return JsonResponse({"message": "Item with this name already exists for this restaurant"}, status=status.HTTP_400_BAD_REQUEST)

        

def delete_menuItem(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == "POST":
        menu_item = get_object_or_404(MenuItem, pk=id)
        menu_item.delete()
        menuItems: QuerySet = MenuItem.objects.select_related("restaurant")
        html_string: str = render_to_string("partial/menuItems_row.html", {"menuItems": menuItems})
        msg: str = "Menu item deleted successfully"
        return JsonResponse({"message": msg, "menuItems": html_string}, status=200)

    return JsonResponse({"message": "Invalid request method"}, status=405) 