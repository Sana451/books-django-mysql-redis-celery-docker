from .models import Book, AdvUser
from .tasks import send_activation_notification

from rest_framework import serializers
from django.contrib.auth import get_user_model


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        send_activation_notification.delay(user.username)
        return user

    class Meta:
        model = AdvUser
        fields = ("id", "username", "email", "password",)
