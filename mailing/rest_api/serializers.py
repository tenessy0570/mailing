from rest_framework import serializers

from .models import Client
from .models import Mailing


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ("id", "text", "datetime_start", "datetime_end", "client_tag")


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ("id", "tag", "phone_number", "mobile_operator_code")
