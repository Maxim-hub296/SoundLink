from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
            return user
        except IntegrityError:
            raise serializers.ValidationError({
                "username": "Пользователь с таким именем уже существует."
            })
