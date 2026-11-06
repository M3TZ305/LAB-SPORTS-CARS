from django.contrib import admin

from .models import Car, PurchaseRequest, TestDriveBooking


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "body_style", "demo_price")
    list_filter = ("year", "body_style")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TestDriveBooking)
class TestDriveBookingAdmin(admin.ModelAdmin):
    list_display = ("car", "city", "date", "slot", "name", "email")
    list_filter = ("car", "city", "date")
    ordering = ("-date", "slot")


@admin.register(PurchaseRequest)
class PurchaseRequestAdmin(admin.ModelAdmin):
    list_display = ("car", "quoted_price", "created_at", "name", "email")
    list_filter = ("car", "created_at")
    readonly_fields = ("quoted_price", "created_at")

    def has_add_permission(self, request):
        return False
