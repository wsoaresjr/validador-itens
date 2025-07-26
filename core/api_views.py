from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ItemUploadSerializer

class UploadLoteAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ItemUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensagem': 'Upload realizado com sucesso.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
