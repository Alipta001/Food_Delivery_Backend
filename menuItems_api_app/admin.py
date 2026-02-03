from django.contrib import admin
from .models import MenuItem, MenuItemImage


# ---------- Inline Images (LIKE RESTAURANT IMAGES) ----------

class MenuItemImageInline(admin.TabularInline):
    model = MenuItemImage
    extra = 1
    min_num = 0
    readonly_fields = ("uploaded_at",)


# ---------- Menu Item Admin ----------

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "restaurant",
        "price",
        "available",
        "image_count",
    )

    list_filter = (
        "restaurant",
        "available",
    )

    search_fields = (
        "name",
        "restaurant__name",
    )

    ordering = ("restaurant", "name")

    list_editable = (
        "available",
    )

    fieldsets = (
        ("Menu Item Details", {
            "fields": (
                "restaurant",
                "name",
                "description",
                "price",
            )
        }),
        ("Availability", {
            "fields": (
                "available",
            )
        }),
    )

    inlines = [
        MenuItemImageInline,
    ]

    def image_count(self, obj):
        return obj.images.count()

    image_count.short_description = "Images"
