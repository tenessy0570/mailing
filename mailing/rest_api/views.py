import loguru
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Client
from .models import Mailing
from .serializers import ClientSerializer
from .serializers import MailingSerializer

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
