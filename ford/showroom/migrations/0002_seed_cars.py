from django.db import migrations


def photo(filename, alt):
    return {"src": f"showroom/images/{filename}.webp", "alt": alt}


def feature(filename, title, description):
    return {
        "src": f"showroom/images/{filename}.webp",
        "title": title,
        "description": description,
    }


CARS = [
    {
        "slug": "taurus",
        "name": "Ford Taurus",
        "year": 2026,
        "body_style": "Sedan",
        "demo_price": 119000,
        "engine": "2.0L EcoBoost",
        "power": "239 hp",
        "transmission": "8-speed automatic",
        "seats": 5,
        "headline": "Everyday Comfort, Confident Power",
        "description": "The Taurus combines a roomy five-seat cabin with a turbocharged engine and a calm, refined ride. It is equally at home on the daily commute and on longer journeys.",
        "gallery": [
            photo("taurus-front", "Ford Taurus from the front three-quarter angle"),
            photo("taurus-rear", "Rear lighting and exterior of the Ford Taurus"),
            photo("taurus-interior", "Ford Taurus cabin and touchscreen"),
            photo("taurus-detail", "Ford Taurus exterior detail"),
        ],
        "features": [
            feature("taurus-interior", "13.2-inch Touchscreen", "Access navigation and compatible phone apps from the central display."),
            feature("taurus-detail", "LED Lighting", "The front and rear lighting give the Taurus a distinctive profile."),
            feature("taurus-rear", "Confident Styling", "A wide stance and sculpted body give the Taurus a composed presence."),
        ],
        "official_url": "https://www.me.ford.com/en/sau/cars/taurus/",
    },
    {
        "slug": "mustang-gt",
        "name": "Ford Mustang GT",
        "year": 2026,
        "body_style": "Fastback",
        "demo_price": 225000,
        "engine": "5.0L Coyote V8",
        "power": "Up to 486 hp",
        "transmission": "10-speed automatic",
        "seats": 4,
        "headline": "The V8 Fastback",
        "description": "The Mustang GT pairs a naturally aspirated 5.0-litre V8 with a digital cockpit and the fastback profile that defines the Mustang. The stated output is for the available active valve performance exhaust.",
        "gallery": [
            photo("mustang-front", "Ford Mustang GT from the front three-quarter angle"),
            photo("mustang-rear", "Ford Mustang GT rear and signature tri-bar lamps"),
            photo("mustang-interior", "Ford Mustang GT driver cockpit"),
            photo("mustang-detail", "Ford Mustang GT exterior detail"),
        ],
        "features": [
            feature("mustang-interior", "Digital Cockpit", "A configurable digital cluster and centre touchscreen put controls in the driver's view."),
            feature("mustang-detail", "Fastback Profile", "A long bonnet and sweeping roofline carry the Mustang shape forward."),
            feature("mustang-rear", "Tri-Bar Taillights", "Three distinct lamps on each side make the Mustang recognizable from behind."),
        ],
        "official_url": "https://www.me.ford.com/en/sau/cars/mustang/",
    },
    {
        "slug": "territory",
        "name": "Ford Territory",
        "year": 2027,
        "body_style": "Crossover SUV",
        "demo_price": 139000,
        "engine": "1.5L turbo hybrid",
        "power": "148 hp petrol engine",
        "transmission": "2-speed hybrid automatic",
        "seats": 5,
        "headline": "Room for the Next Adventure",
        "description": "The Territory is a five-seat crossover with a practical cabin and available hybrid power. The Platinum trim adds features such as a panoramic sunroof and a 360-degree camera.",
        "gallery": [
            photo("territory-front", "Ford Territory Platinum from the front three-quarter angle"),
            photo("territory-rear", "Ford Territory Platinum viewed from behind"),
            photo("territory-interior", "Ford Territory Platinum dashboard and cabin"),
            photo("territory-detail", "Ford Territory Platinum exterior detail"),
        ],
        "features": [
            feature("territory-interior", "Connected Cabin", "A 12-inch centre display brings key controls within easy reach."),
            feature("territory-detail", "Platinum Styling", "A gloss-black grille and 20-inch wheels distinguish the Platinum trim."),
            feature("territory-rear", "Hands-Free Liftgate", "The Platinum trim makes it easier to reach the cargo area with your hands full."),
        ],
        "official_url": "https://www.me.ford.com/en/sau/suvs/territory/",
    },
]


def seed_cars(apps, schema_editor):
    car_model = apps.get_model("showroom", "Car")
    car_model.objects.using(schema_editor.connection.alias).bulk_create(
        [car_model(**car) for car in CARS]
    )


def remove_seed_cars(apps, schema_editor):
    car_model = apps.get_model("showroom", "Car")
    car_model.objects.using(schema_editor.connection.alias).filter(
        slug__in=[car["slug"] for car in CARS]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [("showroom", "0001_initial")]

    operations = [migrations.RunPython(seed_cars, remove_seed_cars)]
