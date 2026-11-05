from django.contrib import admin

from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "body_style", "demo_price")
    list_filter = ("year", "body_style")
    prepopulated_fields = {"slug": ("name",)}
