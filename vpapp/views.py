from django.contrib.auth import get_user_model, authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework import permissions
from rest_framework import status
from vpapp.models import Video
from django.views import View
from .serializers import (
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
    UserAuthSerializer,
    VideoSerializer,
    UserSerializer,
)

class CreateUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return Response(
                    {"error": "A user with that email already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserAuthSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)

                response_data = {"email": email, "token": token.key}

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    def post(self, request, format=None):
        serializer = PasswordResetRequestSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)

            send_mail(
                "Password Reset Request",
                "Click the link below to reset your password \n\n http://localhost:8000/api/reset-password",
                "noreply.vpapp@gmail.com",
                [email],
                fail_silently=False,
            )

            return Response(
                {"message": "Password reset email sent"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    def post(self, request, format=None):
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password reset successful"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoUploadView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, format=None):
        if not request.user.is_staff:
            return Response(
                {"detail": "Only admins can upload videos"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoViewer(View):
    template_name = "video_viewer.html"

    def get(self, request, id=None):
        if not id:
            first_video = Video.objects.order_by("pk").first()
            if first_video:
                return redirect("video-viewer", id=first_video.pk)
            else:
                return render(request, "no_videos.html")

        video = get_object_or_404(Video, pk=id)
        previous_video = Video.objects.filter(pk__lt=id).order_by("-pk").first()
        next_video = Video.objects.filter(pk__gt=id).order_by("pk").first()

        context = {
            "video": video,
            "previous_video": previous_video,
            "next_video": next_video,
        }

        return render(request, self.template_name, context)
