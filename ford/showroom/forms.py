from datetime import date, time, timedelta
from zoneinfo import ZoneInfo

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.translation import gettext_lazy as _

from .models import TestDriveBooking


RIYADH = ZoneInfo("Asia/Riyadh")
SLOTS = [time(hour) for hour in (10, 11, 13, 15, 17)]
SLOT_CHOICES = [("", _("Choose a time"))] + [
    (slot.isoformat(), slot.strftime("%H:%M")) for slot in SLOTS
]


class ContactForm(forms.Form):
    name = forms.CharField(max_length=80, label=_("Full name"))
    email = forms.EmailField(label=_("Email"))


class TestDriveForm(ContactForm):
    city = forms.ChoiceField(label=_("City"), choices=[("", _("Choose a city"))] + TestDriveBooking.City.choices)
    date = forms.TypedChoiceField(
        label=_("Date"),
        coerce=date.fromisoformat,
        error_messages={"invalid_choice": _("Choose a date between tomorrow and 30 days from today.")},
    )
    slot = forms.TypedChoiceField(choices=SLOT_CHOICES, coerce=time.fromisoformat, label=_("Time (Saudi Arabia)"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.localdate(timezone=RIYADH)
        dates = [today + timedelta(days=offset) for offset in range(1, 31)]
        self.fields["date"].choices = [("", _("Choose a date"))] + [
            (day.isoformat(), date_format(day, "l, j F Y")) for day in dates
        ]


class PurchaseForm(ContactForm):
    def clean_email(self):
        return self.cleaned_data["email"].lower()


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = _("Use letters, numbers, or @ . + - _. Spaces are excluded.")
        self.fields["password1"].help_text = _(
            "Use at least 8 characters. Avoid common passwords, numbers alone, and passwords similar to your username."
        )
        self.fields["password2"].help_text = ""
