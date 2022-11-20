from django.db import models

from mailing.mailing.validators import is_digit
from mailing.mailing.validators import tag_exists
from mailing.mailing.validators import timezone_exists


class Mailing(models.Model):
    id = models.IntegerField("id", primary_key=True)
    text = models.TextField("text", required=True, null=False, blank=False)
    datetime_start = models.DateTimeField(
        "Date and time of mailing start",
        required=True,
        blank=False,
        null=False
    )
    datetime_end = models.DateTimeField(
        "Date and time of mailing end",
        required=True,
        blank=False,
        null=False
    )
    client_tag = models.CharField(
        max_length=255,
        required=True,
        null=False,
        blank=False,
        validators=[tag_exists]
    )


class Client(models.Model):
    id = models.IntegerField("id", primary_key=True)
    tag = models.CharField(
        required=True,
        null=False,
        blank=True,
        default="subscriber",
        validators=[tag_exists]
    )
    phone_number = models.CharField(
        max_length=11,
        required=True,
        null=False,
        blank=False,
        validators=[is_digit]
    )
    mobile_operator_code = models.CharField(
        max_length=255,
        required=True,
        null=False,
        blank=False,
        validators=[is_digit]
    )

    # Default is UTC+0
    timezone = models.CharField(
        required=True,
        null=False,
        blank=True,
        default="Europe/London",
        validators=[timezone_exists]
    )


class Message(models.Model):
    id = models.IntegerField("id", primary_key=True)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True, required=True, null=False, blank=True)
    status = models.CharField(required=True, null=False, blank=False)

    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    mailing_id = models.ForeignKey(Mailing, on_delete=models.CASCADE)
