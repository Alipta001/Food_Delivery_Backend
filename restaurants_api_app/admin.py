from django.contrib import admin
from .models import Restaurants, RestaurantImage, Offer


# ---------- Inline Admins ----------

class RestaurantImageInline(admin.TabularInline):
    model = RestaurantImage
    extra = 1


class OfferInline(admin.StackedInline):
    model = Offer
    extra = 0
    max_num = 1


@admin.register(Restaurants)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "cuisine_type",
        "rating",
        "offer_status",
        "created_at",
    )

    list_filter = (
        "cuisine_type",
    )

    search_fields = (
        "name",
        "cuisine_type",
        "address",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "uploaded_at",
    )

    fieldsets = (
        ("Restaurant Details", {
            "fields": (
                "name",
                "address",
                "cuisine_type",
                "rating",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "uploaded_at",
            )
        }),
    )

    inlines = [
        RestaurantImageInline,
        OfferInline,
    ]

    def offer_status(self, obj):
        if hasattr(obj, "offer") and obj.offer.is_active:
            return "Active"
        return "No Offer"

    offer_status.short_description = "Offer"
