from rest_framework import serializers
from .models import Video
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Use the email as the username
        validated_data["username"] = validated_data.get("email")
        # Hash the password before saving the user
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, data):
        if not data.get("email") or not data.get("password"):
            raise serializers.ValidationError("Please provide an email and a password")
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with that email exists")
        return value


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with that email exists")
        return value

    def save(self):
        email = self.validated_data["email"]
        new_password = self.validated_data["new_password"]
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return user


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "description",
            "video_file",
            "upload_date",
            "uploaded_by",
        ]
        read_only_fields = ["id", "upload_date", "uploaded_by"]
