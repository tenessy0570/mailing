import pytz
from django.core.exceptions import ValidationError


def timezone_exists(value):
    if value not in pytz.all_timezones:
        raise ValidationError("This timezone doesn't exist")


def is_digit(value: str):
    if not value.isdigit():
        raise ValidationError("Value should be digit")


def is_a_phone_number(value: str):
    if value[0] != "7":
        raise ValidationError("Phone number should start with 7")


def tag_exists(value):
    allowed_values = ["subscriber", "buyer"]
    if value not in allowed_values:
        raise ValidationError(f"Value is not allowed. List of allowed values: {allowed_values}")
