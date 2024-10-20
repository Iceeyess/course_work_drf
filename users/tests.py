from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from users.models import User
from config import settings

# Create your tests here.
class UserTestCase(APITestCase):
    """Класс тестирования модели пользователя"""
    def setUp(self) -> None:
        # Создание пользователя
        self.user_data = dict(username='test2', password='1234', email='test2@test.ru')
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        """Тест на создание пользователя"""
        data = dict(username='test', password='1234', email='test@test.ru')
        client = APIClient()
        url = reverse('users:user-register')
        response = client.post(path=url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_user(self):
        """Тест на удаление пользователя из setUp"""
        client = APIClient()
        #  Авторизация
        user_id = self.user.id
        auth_url = reverse('users:token')
        access_token = client.post(auth_url, {
            'username': self.user_data.get('username'),
            'password': self.user_data.get('password')
        }).data.get('access')
        client.credentials(HTTP_AUTHORIZATION=f'Token {access_token}')
        headers = {
            'Authorization': f'Token {access_token}',
            'Content-Type': 'application/json'
        }
        auth_url = reverse('users:user-delete', args=[self.user.id])
        response = client.delete(path=auth_url, format='json', headers=headers)
        #  Проверка на статус 204 и, что юзера под сохраненным user_id не существует
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=user_id).exists())

