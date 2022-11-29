from django.db import models

from .validators import is_digit
from .validators import tag_exists
from .validators import timezone_exists


class Mailing(models.Model):
    text = models.TextField("text", null=False, blank=False)
    datetime_start = models.DateTimeField(
        "Date and time of mailing start",
        blank=False,
        null=False
    )
    datetime_end = models.DateTimeField(
        "Date and time of mailing end",
        blank=False,
        null=False
    )
    client_tag = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        validators=[tag_exists]
    )


class Client(models.Model):
    tag = models.CharField(
        null=False,
        blank=True,
        default="subscriber",
        validators=[tag_exists],
        max_length=255
    )
    phone_number = models.CharField(
        max_length=11,
        null=False,
        blank=False,
        validators=[is_digit]
    )
    mobile_operator_code = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        validators=[is_digit]
    )

    # Default is UTC+0
    timezone = models.CharField(
        null=False,
        blank=True,
        default="Europe/London",
        validators=[timezone_exists],
        max_length=255
    )


class Message(models.Model):
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True, null=False, blank=True)
    status = models.CharField(null=False, blank=False, max_length=255)

    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    mailing_id = models.ForeignKey(Mailing, on_delete=models.CASCADE)
