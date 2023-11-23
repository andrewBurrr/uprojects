from abc import ABC

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print("getting token")
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)

        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        profile_image = user.profile_image.url if user.profile_image else ""
        token['profile_image'] = profile_image

        return token


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user = CustomUser(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user
