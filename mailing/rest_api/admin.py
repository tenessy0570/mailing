from django.contrib import admin

from mailing.rest_api.models import Client
from mailing.rest_api.models import Mailing
from mailing.rest_api.models import Message
# Register your models here.

admin.register(Client)
admin.register(Mailing)
admin.register(Message)
