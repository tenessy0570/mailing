from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, UpdateAPIView, get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
import loguru

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


class ClientUpdateAPIView(APIView):
    @staticmethod
    def patch(request: Request, pk: int):
        client_to_update = Client.objects.get(id=pk)
        serialized = ClientSerializer(instance=client_to_update, data=request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            logger.info(f"Updated client with new data: {serialized}")
            return Response({"ok": True, "data": {**serialized.data}}, status=status.HTTP_201_CREATED)

        return Response({"ok": "false", "error": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
