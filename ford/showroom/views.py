from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext as _, gettext_lazy
from django.views.decorators.http import require_http_methods, require_POST

from .forms import PurchaseForm, RegistrationForm, TestDriveForm
from .models import Car, PurchaseRequest, TestDriveBooking

PRICE_RANGES = {
    "under-130000": (gettext_lazy("Under SAR 130,000"), {"demo_price__lt": 130000}),
    "130000-and-up": (gettext_lazy("SAR 130,000 and above"), {"demo_price__gte": 130000}),
}


def home(request):
    cars = list(Car.objects.all()[:3])
    hero_cars = sorted(cars, key=lambda car: car.slug != "mustang-gt")
    return render(request, "showroom/home.html", {"cars": cars, "hero_cars": hero_cars})


def car_list(request):
    cars = Car.objects.order_by("-year", "id")
    selected = {
        key: request.GET.get(key, "").strip()
        for key in ("brand", "model", "price", "year", "q")
    }
    if selected["brand"] and selected["brand"].lower() != "ford":
        cars = cars.none()
    if selected["model"]:
        cars = cars.filter(Q(name__iexact=selected["model"]) | Q(slug__iexact=selected["model"]))
    if selected["price"] in PRICE_RANGES:
        lookup = PRICE_RANGES[selected["price"]][1]
        cars = cars.filter(**lookup)
    if selected["year"]:
        try:
            year = int(selected["year"])
        except ValueError:
            year = 0
        cars = cars.filter(year=year) if 1900 <= year <= 9999 else cars.none()
    if selected["q"]:
        terms = selected["q"][:100].casefold().split()
        matches = [
            pk for pk, name, year in cars.values_list("pk", "name", "year")
            if all(term in f"{name} {_(name)} {year}".casefold() for term in terms)
        ]
        cars = cars.filter(pk__in=matches)

    page = Paginator(cars, 6).get_page(request.GET.get("page"))
    query = request.GET.copy()
    query.pop("page", None)
    model_choices = list(Car.objects.order_by("-year", "name").values_list("slug", "name", "year"))
    filter_models = sorted({name for _, name, _ in model_choices})
    selected_model = next(
        (name for slug, name, _ in model_choices if slug == selected["model"]),
        selected["model"],
    )
    comparison = request.GET.getlist("compare")
    comparison_error = ""
    comparison_cars = []
    if comparison:
        if len(comparison) == 2 and comparison[0] != comparison[1]:
            matched = {car.slug: car for car in Car.objects.filter(slug__in=comparison)}
            if len(matched) == 2:
                comparison_cars = [matched[slug] for slug in comparison]
        if not comparison_cars:
            comparison_error = _("Choose two different cars from the inventory.")

    return render(request, "showroom/car_list.html", {
        "comparison_cars": comparison_cars,
        "comparison_requested": bool(comparison),
        "comparison_error": comparison_error,
        "compare_first": comparison[0] if comparison else "",
        "compare_second": comparison[1] if len(comparison) > 1 else "",
        "page": page,
        "page_numbers": page.paginator.page_range,
        "filter_query": query.urlencode(),
        "selected": selected,
        "models": model_choices,
        "filter_models": filter_models,
        "selected_model": selected_model,
        "years": Car.objects.order_by("-year").values_list("year", flat=True).distinct(),
        "prices": [(key, value[0]) for key, value in PRICE_RANGES.items()],
    })


@require_http_methods(["GET", "HEAD", "POST"])
def car_detail(request, slug):
    car = get_object_or_404(Car, slug=slug)
    detail_tab = request.GET.get("tab", "overview")
    if detail_tab not in {"overview", "specifications", "features"}:
        detail_tab = "overview"
    specs = [
        ("settings", _("Engine"), _(car.engine)),
        ("bolt", _("Power"), _(car.power)),
        ("speed", _("Transmission"), _(car.transmission)),
        ("airline_seat_recline_normal", _("Seats"), car.seats),
    ]
    action = request.POST.get("action", "test-drive") if request.method == "POST" else ""
    if action not in {"", "test-drive", "purchase"}:
        return HttpResponseBadRequest()
    drive_form = TestDriveForm(request.POST if action == "test-drive" else None)
    purchase_form = PurchaseForm(request.POST if action == "purchase" else None, auto_id="purchase_%s")

    if action == "test-drive" and drive_form.is_valid():
        data = drive_form.cleaned_data
        booking, created = TestDriveBooking.objects.get_or_create(
            car=car, city=data["city"], date=data["date"], slot=data["slot"],
            defaults={"name": data["name"], "email": data["email"]},
        )
        if created:
            request.session["detail_confirmation"] = [action, booking.pk]
            return redirect(f"{car.get_absolute_url()}#{action}")
        drive_form.add_error("slot", _("That time is already booked for this car in this city. Choose another time."))

    if action == "purchase" and purchase_form.is_valid():
        data = purchase_form.cleaned_data
        purchase, created = PurchaseRequest.objects.get_or_create(
            car=car, email=data["email"], defaults={"name": data["name"], "quoted_price": car.demo_price},
        )
        if created:
            request.session["detail_confirmation"] = [action, purchase.pk]
            return redirect(f"{car.get_absolute_url()}#{action}")
        purchase_form.add_error("email", _("A purchase request for this car already uses this email."))

    confirmation = None
    if request.method == "GET" and (pending := request.session.get("detail_confirmation")):
        pending_action, pk = pending
        model = TestDriveBooking if pending_action == "test-drive" else PurchaseRequest
        confirmation = model.objects.filter(pk=pk, car=car).first()
        if confirmation:
            action = pending_action
            request.session.pop("detail_confirmation")

    return render(request, "showroom/car_detail.html", {
        "car": car, "specs": specs, "detail_tab": detail_tab, "drive_form": drive_form, "purchase_form": purchase_form,
        "active_action": action, "confirmation": confirmation, "terms": (12, 24, 36, 48, 60),
    })


@require_http_methods(["GET", "HEAD", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect("showroom:login")
    form = RegistrationForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save())
        return redirect("showroom:login")
    return render(request, "showroom/account.html", {"form": form, "registering": True})


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
