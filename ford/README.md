# Ford

A local Django lab based on the desktop and mobile design in the parent folder. The showroom contains the 2026 Ford Taurus, 2026 Ford Mustang GT, and 2027 Ford Territory. Prices and newsletter signup are for demonstration.

## Run on Windows

Open PowerShell in this folder. If `.venv` is already present, run:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Open [the local site](http://127.0.0.1:8000/).

If you are setting up a fresh copy, create the environment and install its dependencies first. Use Python 3.12 or 3.13.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Project layout

- `config/` contains the Django project settings and root URL configuration.
- `showroom/` contains the views, URL mapping, and `Car` model. Migrations create the SQLite schema and populate the three cars.
- `showroom/templates/showroom/` contains `base.html`, the page templates, and the shared car card.
- `showroom/static/showroom/` contains styles, JavaScript, photos, and locally served Google fonts and icons.

## Lab features

- The home, inventory, details and about views render inherited templates. The three car pages share a detail template.
- Template links use named URLs. `Car.get_absolute_url()` resolves a detail URL from the model.
- `/cars/taurus/` passes the model slug as a path parameter. `/cars/?year=2026` filters the inventory via a query parameter.
- The header theme button posts to Django and persists the preference in the `ford_theme` cookie.
- The gallery, search, and mobile menu work locally. The wishlist is stored in the browser.

## Vehicle specifications

- [Taurus on Ford Saudi Arabia](https://www.me.ford.com/en/sau/cars/taurus/) and [Al Jazirah Ford](https://ar.aljazirahford.com/vehicles/2026-ford-taurus/)
- [Mustang on Ford Saudi Arabia](https://www.me.ford.com/en/sau/cars/mustang/) and [Al Jazirah Ford](https://en.aljazirahford.com/vehicles/2026-ford-mustang/)
- [Territory on Ford Saudi Arabia](https://www.me.ford.com/en/sau/suvs/territory/)
