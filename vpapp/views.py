from rest_framework import status
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from .serializers import UserAuthSerializer, PasswordResetRequestSerializer, PasswordResetSerializer, UserSerializer, VideoSerializer
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
    serializer = UserAuthSerializer(data=request.data)
    
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


class PasswordResetRequestView(APIView):
  def post(self, request, format=None):
    serializer = PasswordResetRequestSerializer(data=request.data)
    
    if serializer.is_valid():
      email = serializer.validated_data['email']
      user = User.objects.get(email=email)
      
      send_mail(
        'Password Reset Request',
        'Click the link below to reset your password \n\n http://localhost:8000/api/reset-password',
        'noreply.vpapp@gmail.com',
        [email],
        fail_silently=False
      )
      
      return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  

class PasswordResetView(APIView):
  def post(self, request, format=None):
    serializer = PasswordResetSerializer(data=request.data)
    
    if serializer.is_valid():
      serializer.save()
      return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  

class VideoUploadView(APIView):
  permission_classes = [permissions.IsAdminUser]
  
  def post(self, request, format=None):
    if not request.user.is_staff:
      return Response({'detail': 'Only admins can upload videos'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = VideoSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(uploaded_by=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  