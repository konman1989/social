from django.contrib.auth import login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id",
                  "email",
                  "first_name",
                  "last_name"]


class UserActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id",
                  "last_login",
                  "last_request"]


class CreateUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id",
                  "email",
                  "first_name",
                  "last_name",
                  "password1",
                  "password2"]

    def validate_password2(self, value):
        password1 = self.initial_data.get('password1')

        if password1 != value:
            raise serializers.ValidationError("Passwords don't match!")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomTokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        login(self.context['request'], self.user)
        return data


