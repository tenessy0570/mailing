import pytz
from django.core.exceptions import ValidationError


def timezone_exists(value):
    if value not in pytz.all_timezones:
        raise ValidationError


def is_digit(value: str):
    if not value.isdigit():
        raise ValidationError


def tag_exists(value):
    if value not in ["subscriber", "buyer"]:
        raise ValidationError
