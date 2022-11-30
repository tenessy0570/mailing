from django.urls import path

from . import views


urlpatterns = [
    path('client', views.ClientCreateAPIView.as_view(), name="client_create"),
    path('client/<int:pk>', views.ClientUpdateAndDeleteAPIView.as_view(), name="client_update_and_delete"),
    path('mailing', views.MailingCreateAPIView.as_view(), name="mailing_create"),
    path('mailing/<int:pk>', views.MailingUpdateAndDeleteAPIView.as_view(), name="mailing_update_and_delete"),
    path('mailing/<int:pk>/messages', views.MailingSentMessagesListAPIView.as_view(), name="mailing_sent_messages"),
    path('mailings_stats', views.StatisticsAboutSentMessagesAPIView.as_view(), name="mailings_stats")
]
