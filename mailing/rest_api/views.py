import loguru
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Client
from .models import Mailing
from .models import Message
from .serializers import ClientSerializer
from .serializers import MailingSerializer
from .serializers import MessageSerializer

logger = loguru.logger


class ClientCreateAPIView(CreateAPIView):
    @staticmethod
    def post(request: Request, *args, **kwargs):
        serialized = ClientSerializer(data=request.data)

        if serialized.is_valid():
            serialized.save()
            logger.info(f"Created client: {serialized.data}")
            return Response({"ok": True, "data": {**serialized.data}}, status=status.HTTP_201_CREATED)

        return Response({"ok": "false", "error": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)


class ClientUpdateAndDeleteAPIView(APIView):
    @staticmethod
    def patch(request: Request, pk: int):
        client_to_update = Client.objects.get(id=pk)
        serialized = ClientSerializer(instance=client_to_update, data=request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            logger.info(f"Updated client with new data: {serialized.data}")
            return Response({"ok": True, "data": {**serialized.data}}, status=status.HTTP_201_CREATED)

        return Response({"ok": "false", "error": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request: Request, pk: int):
        client_to_delete: Client = get_object_or_404(Client, id=pk)
        logger.info(f"Deleting client with id: {client_to_delete.pk}...")

        client_to_delete.delete()
        return Response({"ok": "true"}, status=status.HTTP_200_OK)


class MailingCreateAPIView(APIView):
    @staticmethod
    def post(request: Request):
        serialized = MailingSerializer(data=request.data)

        if serialized.is_valid():
            serialized.save()
            logger.info(f"Created mailing: {serialized.data}")

            # TODO: scheduled_mailing.append_new_mailing(serialized)
            return Response({"ok": True, "data": {**serialized.data}}, status=status.HTTP_201_CREATED)

        return Response({"ok": "false", "error": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)


class MailingUpdateAndDeleteAPIView(APIView):
    @staticmethod
    def patch(request: Request, pk: int):
        mailing_to_update = Mailing.objects.get(id=pk)
        serialized = MailingSerializer(instance=mailing_to_update, data=request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            logger.info(f"Updated mailing with new data: {serialized.data}")
            return Response({"ok": True, "data": {**serialized.data}}, status=status.HTTP_201_CREATED)

        return Response({"ok": "false", "error": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request: Request, pk: int):
        mailing_to_delete: Client = get_object_or_404(Client, id=pk)
        logger.info(f"Deleting mailing with id: {mailing_to_delete.pk}...")

        mailing_to_delete.delete()

        # TODO: scheduled_mailing.delete_existing_mailing(mailing_to_delete)
        return Response({"ok": "true"}, status=status.HTTP_200_OK)


class MailingSentMessagesListAPIView(APIView):
    @staticmethod
    def get(request: Request, pk: int):
        messages = Message.objects.filter(mailing_id=pk)
        serialized = MessageSerializer(messages, many=True)

        return Response({"ok": True, "data": (data for data in serialized.data)}, status=status.HTTP_200_OK)


class StatisticsAboutSentMessagesAPIView(APIView):
    @staticmethod
    def get(request: Request):
        mailings = Mailing.objects.all()
        messages = Message.objects.all().select_related('mailing')  # Avoid 1000 queries in loop below

        list_of_mailings_with_messages_statistic = []

        # Cringe method, I know
        for mailing in mailings:
            success_messages_count = 0
            failed_messages_count = 0

            for message in messages:
                if message.mailing.id != mailing.id:
                    continue

                success_messages_count += int(message.status == "success")
                failed_messages_count += int(message.status == "failed")

            serialized = MailingSerializer(mailing)
            mailing_with_messages_stats = {
                **serialized.data,
                "messages": {
                    "success": success_messages_count,
                    "failed": failed_messages_count
                }
            }
            list_of_mailings_with_messages_statistic.append(mailing_with_messages_stats)

        return Response({"ok": True, "data": list_of_mailings_with_messages_statistic})
