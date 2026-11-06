from django.db import migrations


CARS = [
    {
        "name": "Ford Mustang Dark Horse",
        "slug": "mustang-dark-horse",
        "year": 2025,
        "body_style": "Coupe",
        "demo_price": 275000,
        "engine": "5.0L Coyote V8",
        "power": "500 hp (US spec)",
        "transmission": "6-speed manual",
        "seats": 4,
        "headline": "A Mustang built for the track",
        "description": "The Dark Horse pairs a modified Coyote V8 with a TREMEC manual gearbox and MagneRide adaptive damping.",
        "gallery": [
            {"src": "showroom/images/dark-horse-front.webp", "alt": "Ford Mustang Dark Horse exterior"},
            {"src": "showroom/images/dark-horse-cabin.webp", "alt": "Mustang Dark Horse cockpit and manual shifter"},
        ],
        "features": [
            {"src": "showroom/images/dark-horse-cabin.webp", "title": "Six-Speed Manual", "description": "The TREMEC gearbox offers rev matching for smoother downshifts."},
            {"src": "showroom/images/dark-horse-front.webp", "title": "MagneRide Damping", "description": "Adaptive dampers adjust to changing road conditions."},
        ],
        "official_url": "https://www.ford.com/cars/mustang/2025/models/dark-horse/",
    },
    {
        "name": "Ford F-150 Raptor",
        "slug": "f-150-raptor",
        "year": 2025,
        "body_style": "Pickup",
        "demo_price": 315000,
        "engine": "3.5L High-Output EcoBoost V6",
        "power": "420 hp (Saudi spec)",
        "transmission": "10-speed automatic",
        "seats": 5,
        "headline": "Performance beyond the pavement",
        "description": "The F-150 Raptor combines a turbocharged V6 with off-road suspension and selectable drive modes for loose surfaces.",
        "gallery": [
            {"src": "showroom/images/raptor-front.webp", "alt": "Ford F-150 Raptor on desert terrain"},
            {"src": "showroom/images/raptor-trail.webp", "alt": "Blue Ford F-150 Raptor driving on a dirt trail"},
        ],
        "features": [
            {"src": "showroom/images/raptor-front.webp", "title": "High-Output EcoBoost", "description": "The twin-turbo V6 delivers 420 horsepower in the Saudi-market configuration."},
            {"src": "showroom/images/raptor-trail.webp", "title": "Baja Mode", "description": "A selectable drive mode tuned for loose off-road terrain."},
        ],
        "official_url": "https://en.aljazirahford.com/vehicles/2025-ford-f-150-raptor/",
    },
]


def add_cars(apps, schema_editor):
    cars = apps.get_model("showroom", "Car").objects.using(schema_editor.connection.alias)
    cars.bulk_create([cars.model(**car) for car in CARS])


def remove_cars(apps, schema_editor):
    cars = apps.get_model("showroom", "Car").objects.using(schema_editor.connection.alias)
    cars.filter(slug__in=[car["slug"] for car in CARS]).delete()


class Migration(migrations.Migration):
    dependencies = [("showroom", "0003_test_drive_booking")]
    operations = [migrations.RunPython(add_cars, remove_cars)]
