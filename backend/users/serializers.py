from abc import ABC

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser, Owner


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print("getting token")
        token = super().get_token(user)

        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['profile_image'] = str(user.profile_image.url if user.profile_image else None)

        return token


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    

    def save(self, **kwargs):
        owner = Owner.objects.create()
        
        user = CustomUser(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            owner_id=owner,
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user
