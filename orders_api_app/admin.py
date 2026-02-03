from django.contrib import admin
from .models import Order, OrderItem


# ---------- Order Items Inline ----------

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("menu_item", "quantity", "price")
    can_delete = False


# ---------- Order Admin ----------

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "restaurant",
        "totalAmount",
        "status",
        "createdAt",
    )

    list_filter = (
        "status",
        "restaurant",
    )

    search_fields = (
        "id",
        "user__email",
        "restaurant__name",
    )

    list_editable = (
        "status",
    )

    ordering = ("-createdAt",)

    readonly_fields = (
        "user",
        "restaurant",
        "totalAmount",
        "createdAt",
    )

    fieldsets = (
        ("Order Info", {
            "fields": (
                "user",
                "restaurant",
                "totalAmount",
                "createdAt",
            )
        }),
        ("Order Status", {
            "fields": (
                "status",
            )
        }),
    )

    inlines = [OrderItemInline]


# ---------- Order Item Admin ----------

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "menu_item",
        "quantity",
        "price",
    )

    list_filter = (
        "order__restaurant",
    )

    search_fields = (
        "order__id",
        "menu_item__name",
    )
    ordering = ("-order__createdAt",)