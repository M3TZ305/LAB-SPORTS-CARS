from django.urls import path

from . import views

app_name = "showroom"

urlpatterns = [
    path("", views.home, name="home"),
    path("cars/", views.car_list, name="car_list"),
    path("cars/<slug:slug>/", views.car_detail, name="car_detail"),
    path("about/", views.about, name="about"),
    path("theme/", views.set_theme, name="set_theme"),
]
