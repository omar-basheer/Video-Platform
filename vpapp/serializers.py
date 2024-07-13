from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
      model = User
      fields = ('email', 'password')
      extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
      # Use the email as the username 
      validated_data['username'] = validated_data.get('email') 
      # Hash the password before saving the user
      validated_data['password'] = make_password(validated_data['password'])
      return super().create(validated_data)
    
  
class CustomTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    def validate(self, data):
      if not data.get('email') or not data.get('password'):
        raise serializers.ValidationError("Please provide an email and a password")
      return data
    
    