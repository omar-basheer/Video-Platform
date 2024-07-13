from rest_framework import status
from rest_framework.views import APIView
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .serializers import CustomTokenSerializer, UserSerializer
from django.contrib.auth import get_user_model, authenticate, login

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
      
class LoginUser(APIView):
  permission_classes = [AllowAny]
  def post(self, request, format=None):
    serializer = CustomTokenSerializer(data=request.data)
    
    if serializer.is_valid():
      email = serializer.validated_data['email']
      password = serializer.validated_data['password']
      
      user = authenticate(request, username=email, password=password)
      if user:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        
        response_data = {
          'email': email,
          'token': token.key
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
      else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
      
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
