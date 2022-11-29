from django.urls import path
from . import views


urlpatterns = [
    path('client', views.ClientApiView.as_view(), name="client_endpoint"),
]
