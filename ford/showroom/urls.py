from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from . import views

app_name = "showroom"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="showroom:home", query_string=True)),
    path("home/", views.home, name="home"),
    path(
        "account/",
        auth_views.LoginView.as_view(
            template_name="showroom/account.html",
            next_page=reverse_lazy("showroom:login"),
        ),
        name="login",
    ),
    path("account/register/", views.register, name="register"),
    path("account/logout/", auth_views.LogoutView.as_view(next_page=reverse_lazy("showroom:home")), name="logout"),
    path("cars/", views.car_list, name="car_list"),
    path("cars/<slug:slug>/", views.car_detail, name="car_detail"),
    path("about/", views.about, name="about"),
    path("theme/", views.set_theme, name="set_theme"),
]
