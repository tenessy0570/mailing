from django.urls import path

from . import views


urlpatterns = [
    path('client', views.ClientCreateAPIView.as_view(), name="client_create"),
    path('client/<int:pk>', views.ClientUpdateAndDeleteAPIView.as_view(), name="client_update_and_delete")
]
