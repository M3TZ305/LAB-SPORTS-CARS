from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .models import Car

PRICE_RANGES = {
    "under-130000": ("Under SAR 130,000", {"demo_price__lt": 130000}),
    "130000-and-up": ("SAR 130,000 and above", {"demo_price__gte": 130000}),
}


def home(request):
    return render(request, "showroom/home.html", {"cars": Car.objects.all()[:3]})


def car_list(request):
    cars = Car.objects.all()
    selected = {
        key: request.GET.get(key, "").strip()
        for key in ("brand", "model", "price", "year", "q")
    }
    if selected["brand"] and selected["brand"].lower() != "ford":
        cars = cars.none()
    if selected["model"]:
        cars = cars.filter(slug=selected["model"])
    if selected["price"] in PRICE_RANGES:
        _, lookup = PRICE_RANGES[selected["price"]]
        cars = cars.filter(**lookup)
    if selected["year"]:
        try:
            year = int(selected["year"])
        except ValueError:
            year = 0
        cars = cars.filter(year=year) if 1900 <= year <= 9999 else cars.none()
    if selected["q"]:
        cars = cars.filter(name__icontains=selected["q"][:100])

    page = Paginator(cars, 6).get_page(request.GET.get("page"))
    query = request.GET.copy()
    query.pop("page", None)
    return render(request, "showroom/car_list.html", {
        "page": page,
        "page_numbers": page.paginator.page_range,
        "filter_query": query.urlencode(),
        "selected": selected,
        "models": Car.objects.values_list("slug", "name"),
        "years": Car.objects.order_by("-year").values_list("year", flat=True).distinct(),
        "prices": [(key, value[0]) for key, value in PRICE_RANGES.items()],
    })


def car_detail(request, slug):
    car = get_object_or_404(Car, slug=slug)
    specs = [
        ("settings", "Engine", car.engine),
        ("bolt", "Power", car.power),
        ("speed", "Transmission", car.transmission),
        ("airline_seat_recline_normal", "Seats", car.seats),
    ]
    return render(request, "showroom/car_detail.html", {"car": car, "specs": specs})


def about(request):
    return render(request, "showroom/about.html")


@require_POST
def set_theme(request):
    target = request.POST.get("next", "")
    if not target.startswith("/") or not url_has_allowed_host_and_scheme(
        target, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        target = reverse("showroom:home")
    response = redirect(target)
    theme = request.POST.get("theme")
    if theme in {"light", "dark"}:
        response.set_cookie(
            "ford_theme", theme, max_age=60 * 60 * 24 * 365,
            httponly=True, samesite="Lax", secure=request.is_secure(),
        )
    return response
