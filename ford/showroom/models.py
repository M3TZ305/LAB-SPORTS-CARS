from django.db import models
from django.urls import reverse


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
        return f"SAR {self.demo_price:,}"
