from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
import loguru

from .serializers import ClientSerializer

logger = loguru.logger


class ClientApiView(APIView):
    @staticmethod
    def post(request: Request):
        client = ClientSerializer(data=request.data)

        if client.is_valid():
            client.save()
            logger.info(f"Created client: {client}")
            return Response({"ok": True, "data": {**client.data}}, status=status.HTTP_201_CREATED)

        return Response({"ok": "false", "error": client.errors}, status=status.HTTP_400_BAD_REQUEST)
