from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Кастомный класс сериализатора токена"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token['username'] = user.username
        token['email'] = user.email

        return token

class UserSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для регистрации пользователя"""
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        """Шифрование пароля при создании"""
        user = super().create(validated_data)
        user.set_password(user.password)
        user.save()
        return user
