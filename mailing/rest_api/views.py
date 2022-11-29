import loguru
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Client
from .serializers import ClientSerializer

logger = loguru.logger


class ClientCreateAPIView(CreateAPIView):
    @staticmethod
    def post(request: Request, *args, **kwargs):
        client = ClientSerializer(data=request.data)

        if client.is_valid():
            client.save()
            logger.info(f"Created client: {client}")
            return Response({"ok": True, "data": {**client.data}}, status=status.HTTP_201_CREATED)

        return Response({"ok": "false", "error": client.errors}, status=status.HTTP_400_BAD_REQUEST)


class ClientUpdateAndDeleteAPIView(APIView):
    @staticmethod
    def patch(request: Request, pk: int):
        client_to_update = Client.objects.get(id=pk)
        serialized = ClientSerializer(instance=client_to_update, data=request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            logger.info(f"Updated client with new data: {serialized}")
            return Response({"ok": True, "data": {**serialized.data}}, status=status.HTTP_201_CREATED)

        return Response({"ok": "false", "error": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request: Request, pk: int):
        client_to_delete: Client = get_object_or_404(Client, id=pk)
        logger.info(f"Deleting client with id: {client_to_delete.pk}...")

        client_to_delete.delete()
        return Response({"ok": "true"}, status=status.HTTP_200_OK)
