from rest_framework import status
from .serializers import UserSerializer
from rest_framework.views import APIView
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class CreateUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
          try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
          except IntegrityError as e:
            return Response({"error": "A user with that email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)