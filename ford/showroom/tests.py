from datetime import timedelta

from django.conf import settings
from django.contrib.staticfiles import finders
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import RIYADH
from .models import Car, PurchaseRequest, TestDriveBooking


class ShowroomFeaturesTests(TestCase):
    def test_comparison_uses_selected_order_and_rejects_invalid_pairs(self):
        url = reverse("showroom:car_list")
        pair = ["f-150-raptor", "mustang-dark-horse"]
        response = self.client.get(url, {"compare": pair})
        self.assertEqual([car.slug for car in response.context["comparison_cars"]], pair)
        self.assertContains(response, "420 hp (Saudi spec)")
        self.assertContains(response, "500 hp (US spec)")

        for invalid_pair in ([pair[0], pair[0]], [pair[0], "unknown"], [pair[0]]):
            with self.subTest(pair=invalid_pair):
                response = self.client.get(url, {"compare": invalid_pair})
                self.assertContains(response, "Choose two different cars")
                self.assertEqual(response.context["comparison_cars"], [])

    def test_inventory_has_a_car_for_each_year_and_its_photos(self):
        years = set(Car.objects.values_list("year", flat=True))
        self.assertTrue(set(range(2010, 2028)).issubset(years))
        for car in Car.objects.filter(year__range=(2010, 2024)):
            with self.subTest(car=car.slug):
                self.assertGreaterEqual(len(car.gallery), 2)
                self.assertTrue(all(finders.find(photo["src"]) for photo in car.gallery))
        response = self.client.get(reverse("showroom:car_list"), {"year": "2010"})
        self.assertEqual([car.slug for car in response.context["page"]], ["mustang-gt-2010"])

    def test_test_drive_confirmations_and_conflicts_are_city_specific(self):
        car = Car.objects.get(slug="mustang-dark-horse")
        url = car.get_absolute_url()
        tomorrow = timezone.localdate(timezone=RIYADH) + timedelta(days=1)
        form = {
            "action": "test-drive", "name": "Demo Visitor", "email": "demo@example.com",
            "city": "riyadh", "date": tomorrow, "slot": "10:00:00",
        }
        response = self.client.post(url, form, follow=True)
        self.assertRedirects(response, f"{url}#test-drive")
        self.assertContains(response, "confirmed in Riyadh")
        self.assertNotContains(self.client.get(url), "confirmed in Riyadh")

        response = self.client.post(url, {**form, "email": "second@example.com"})
        self.assertContains(response, "That time is already booked")
        self.assertEqual(response.context["active_action"], "test-drive")
        self.assertEqual(TestDriveBooking.objects.get(car=car).email, form["email"])

        response = self.client.post(url, {**form, "city": "jeddah"}, follow=True)
        self.assertContains(response, "confirmed in Jeddah")
        other_car = Car.objects.get(slug="f-150-raptor")
        self.assertEqual(self.client.post(other_car.get_absolute_url(), form).status_code, 302)
        self.assertEqual(TestDriveBooking.objects.count(), 3)

    def test_test_drive_rejects_out_of_range_dates_unknown_slots_and_unknown_cities(self):
        car = Car.objects.get(slug="f-150-raptor")
        today = timezone.localdate(timezone=RIYADH)
        form = {
            "name": "Demo Visitor", "email": "demo@example.com",
            "city": "invalid", "date": today, "slot": "01:00:00",
        }
        response = self.client.post(car.get_absolute_url(), form)
        self.assertContains(response, "Choose a date between tomorrow and 30 days from today.")
        self.assertEqual(set(response.context["drive_form"].errors), {"city", "date", "slot"})
        self.assertFalse(TestDriveBooking.objects.exists())

    def test_cash_purchase_keeps_the_price_and_rejects_duplicate_requests(self):
        car = Car.objects.get(slug="mustang-gt")
        url = car.get_absolute_url()
        form = {"action": "purchase", "name": "Demo Buyer", "email": "Buyer@example.com"}
        response = self.client.post(url, form, follow=True)
        self.assertRedirects(response, f"{url}#purchase")
        self.assertContains(response, "Demo purchase request #")
        self.assertEqual(PurchaseRequest.objects.get(car=car).quoted_price, car.demo_price)
        duplicate = self.client.post(url, {**form, "email": form["email"].lower()})
        self.assertContains(duplicate, "already uses this email")
        self.assertEqual(duplicate.context["active_action"], "purchase")
        self.assertEqual(PurchaseRequest.objects.count(), 1)

    def test_language_switch_localizes_content_and_arabic_search(self):
        car = Car.objects.get(slug="mustang-gt-2010")
        response = self.client.post(
            reverse("set_language"), {"language": "ar", "next": car.get_absolute_url()}, follow=True,
        )
        self.assertEqual(self.client.cookies[settings.LANGUAGE_COOKIE_NAME].value, "ar")
        self.assertContains(response, 'lang="ar" dir="rtl"')
        self.assertContains(response, "فورد موستانج جي تي")
        self.assertContains(response, "شراء نقدًا")
        self.assertContains(response, "اختر المدينة")
        self.assertContains(response, "الدفعة الأولى")
        search = self.client.get(reverse("showroom:car_list"), {"q": "موستانج 2010"})
        self.assertEqual([vehicle.slug for vehicle in search.context["page"]], [car.slug])

    def test_inventory_filters_intersect_model_year_and_search(self):
        url = reverse("showroom:car_list")
        params = {"model": "Ford Mustang GT", "year": "2010", "q": "Mustang"}
        response = self.client.get(url, params)
        self.assertEqual([car.slug for car in response.context["page"]], ["mustang-gt-2010"])
        self.assertContains(response, "data-inventory-filters")
        self.assertNotContains(response, 'id="compare" open')
        self.assertFalse(self.client.get(url, {**params, "q": "Raptor"}).context["page"].object_list)

        response = self.client.get(url, {"model": "mustang-gt"})
        self.assertEqual([car.slug for car in response.context["page"]], ["mustang-gt"])
        response = self.client.get(url, {"compare": ["mustang-gt-2010", "mustang-gt-2018"]})
        self.assertContains(response, 'id="compare" open')

    def test_vehicle_tabs_render_only_the_selected_section(self):
        for car in Car.objects.all():
            for tab in ("overview", "specifications", "features"):
                with self.subTest(car=car.slug, tab=tab):
                    response = self.client.get(car.get_absolute_url(), {"tab": tab})
                    self.assertContains(response, f'id="{tab}"')
                    for other in {"overview", "specifications", "features"} - {tab}:
                        self.assertNotContains(response, f'id="{other}"')


    def test_local_account_registration_login_and_logout(self):
        from django.contrib.auth import get_user_model

        login_url = reverse("showroom:login")
        register_url = reverse("showroom:register")
        logout_url = reverse("showroom:logout")
        password = "Test-password-4781"
        self.assertContains(self.client.get(login_url), register_url)
        response = self.client.post(register_url, {
            "username": "showroom-visitor", "password1": password, "password2": password,
        })
        self.assertRedirects(response, login_url)
        user = get_user_model().objects.get(username="showroom-visitor")
        self.assertNotEqual(user.password, password)
        self.assertEqual(self.client.session["_auth_user_id"], str(user.pk))
        self.assertEqual(self.client.get(logout_url).status_code, 405)
        self.assertRedirects(self.client.post(logout_url), reverse("showroom:home"))
        self.assertNotIn("_auth_user_id", self.client.session)

        response = self.client.post(login_url, {
            "username": user.username, "password": password, "next": "https://example.com/",
        })
        self.assertRedirects(response, login_url)
        self.assertContains(self.client.get(login_url), user.username)

    def test_home_has_a_named_url_and_root_redirect(self):
        self.assertEqual(reverse("showroom:home"), "/home/")
        self.assertRedirects(self.client.get("/"), "/home/")
        self.assertRedirects(self.client.get("/home"), "/home/", status_code=301)
        self.assertContains(self.client.get("/home/"), 'data-hero-video')
