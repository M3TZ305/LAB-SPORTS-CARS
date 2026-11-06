# Ford

A local Django showroom with 20 Ford entries covering every model year from 2010 through 2027. Prices, cash purchase requests, financing estimates, test-drive bookings, and newsletter signup are for demonstration.

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
- `showroom/` contains the views, URL mapping, and `Car` model. Migrations create the SQLite schema and populate the inventory.
- `showroom/templates/showroom/` contains `base.html`, the page templates, and the shared car card.
- `showroom/static/showroom/` contains styles, JavaScript, photos, and locally served Google fonts and icons.

## Lab features

- The home, inventory, details and about views render inherited templates. The three car pages share a detail template.
- Template links use named URLs. `Car.get_absolute_url()` resolves a detail URL from the model.
- `/cars/taurus/` passes the model slug as a path parameter. `/cars/?year=2026` filters the inventory via a query parameter.
- The header theme button posts to Django and persists the preference in the `ford_theme` cookie.
- The gallery, search, and mobile menu work locally. The wishlist is stored in the browser.

- All Cars compares two models via repeated query parameters, for example /cars/?compare=mustang-gt&compare=mustang-dark-horse#compare.
- Each detail page includes a full-screen photo viewer and a monthly estimate using the demo price, down payment, term, and annual rate.
- The header language toggle switches between English and Arabic, including right-to-left layout, vehicle information, forms and date labels. The language cookie preserves the choice. The Arabic PO source and compiled MO live in the showroom locale directory.
- Each vehicle has separate links for cash purchase, test-drive booking and installment estimates. The URL fragment opens the selected panel and scrolls to it.
- Test drives use Saudi time and offer six city choices. Bookings and purchase requests are saved in SQLite and can be reviewed in Django admin.
- Archival photo attribution is retained in the gallery records in the inventory data migration. Vehicle information links point to the reference used for each model.

## Vehicle specifications

- [Taurus on Ford Saudi Arabia](https://www.me.ford.com/en/sau/cars/taurus/) and [Al Jazirah Ford](https://ar.aljazirahford.com/vehicles/2026-ford-taurus/)
- [Mustang on Ford Saudi Arabia](https://www.me.ford.com/en/sau/cars/mustang/) and [Al Jazirah Ford](https://en.aljazirahford.com/vehicles/2026-ford-mustang/)
- [Territory on Ford Saudi Arabia](https://www.me.ford.com/en/sau/suvs/territory/)
- [Mustang Dark Horse on Ford US](https://www.ford.com/cars/mustang/2025/models/dark-horse/)
- [F-150 Raptor on Al Jazirah Ford](https://en.aljazirahford.com/vehicles/2025-ford-f-150-raptor/)

## Additional vehicle photos

- Mustang Dark Horse exterior from [Bayou Ford](https://www.bayouford.net/2025-ford-mustang.html) and cabin from [EV-Cars](https://www.ev-cars.pl/en-us/ford-mustang-dark-horse-rental/).
- F-150 Raptor exterior from [Al Jazirah Ford](https://en.aljazirahford.com/vehicles/2025-ford-f-150-raptor/) and trail photo from [Pioneer Ford](https://www.pioneerfordmarietta.com/2025-ford-f-150-vs-toyota-tundra-marietta-oh.html).
