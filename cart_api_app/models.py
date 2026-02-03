# from django.db import models
# from users_api_app.models import User
# from menuItems_api_app.models import MenuItem

# class Cart(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Cart of {self.user}"


# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
#     menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="cart_items")
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"{self.quantity} of {self.menu_item.name} in {self.cart}"

from django.db import models
from users_api_app.models import User
from menuItems_api_app.models import MenuItem


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_amount(self):
        return sum(
            item.price * item.quantity
            for item in self.cart_items.all()
        )

    def __str__(self):
        return f"Cart of {self.user.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()  # snapshot price

    class Meta:
        unique_together = ("cart", "menu_item")

    def __str__(self):
        return f"{self.quantity} × {self.menu_item.name}"
