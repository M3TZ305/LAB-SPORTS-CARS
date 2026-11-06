from django.db import models
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _


class Car(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    year = models.PositiveSmallIntegerField()
    body_style = models.CharField(max_length=40)
    demo_price = models.PositiveIntegerField()
    engine = models.CharField(max_length=80)
    power = models.CharField(max_length=40)
    transmission = models.CharField(max_length=80)
    seats = models.PositiveSmallIntegerField()
    headline = models.CharField(max_length=100)
    description = models.TextField()
    gallery = models.JSONField(default=list)
    features = models.JSONField(default=list)
    official_url = models.URLField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.year} {self.name}"

    def get_absolute_url(self):
        return reverse("showroom:car_detail", kwargs={"slug": self.slug})

    @property
    def price_display(self):
        return gettext("SAR %(amount)s") % {"amount": f"{self.demo_price:,}"}


class TestDriveBooking(models.Model):
    class City(models.TextChoices):
        RIYADH = "riyadh", _("Riyadh")
        JEDDAH = "jeddah", _("Jeddah")
        DAMMAM = "dammam", _("Dammam")
        MAKKAH = "makkah", _("Makkah")
        MADINAH = "madinah", _("Madinah")
        ABHA = "abha", _("Abha")

    city = models.CharField(max_length=12, choices=City.choices, default=City.RIYADH)
    car = models.ForeignKey(Car, on_delete=models.PROTECT)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    date = models.DateField()
    slot = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["car", "city", "date", "slot"], name="unique_city_test_drive_slot"),
        ]

    def __str__(self):
        return f"{self.car} · {self.date} {self.slot:%H:%M}"


class PurchaseRequest(models.Model):
    car = models.ForeignKey(Car, on_delete=models.PROTECT)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    quoted_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["car", "email"], name="unique_car_purchase_email"),
        ]

    def __str__(self):
        return f"{self.car} · #{self.pk}"
