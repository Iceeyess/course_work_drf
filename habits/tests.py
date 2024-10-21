import datetime
import pytz
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse, reverse_lazy
import json
from config.settings import TIME_ZONE
from habits.models import Habit
from users.models import User


# Create your tests here.


class HabitTestCase(APITestCase):
    """Тестирование модели Habit"""

    def setUp(self) -> None:
        # Создание пользователя
        self.user_date = dict(username='test', password='1234', email='test@test.ru')
        self.user_date_2 = dict(username='test2', password='1234', email='test2@test.ru')
        self.client = APIClient()
        self.user = User.objects.create_user(**self.user_date)
        self.user_2 = User.objects.create_user(**self.user_date_2)
        #   auth user
        self.auth_url = reverse('users:token')
        self.access_token = self.client.post(self.auth_url, {
            'username': self.user_date.get('username'),
            'password': self.user_date.get('password')
        }).data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.access_token}')
        self.headers = {
            'Authorization': f'Token {self.access_token}',
            'Content-Type': 'application/json'
        }
        self.data = {
            "user_id": self.user.id,
            "place": "улица",
            "time": "20:00:00",
            "activity": "прогулка",
            "regularity": '1',
            "time_spent": "00:01:59",
            "is_public": True
        }
        self.habit = Habit.objects.create(**self.data)
        print(self.habit)

    def test_create_habit_1(self):
        """Тестирование создание привычек"""
        habit_url = reverse_lazy('habits:habit-list')
        response = self.client.post(path=habit_url, format='json', data=self.data, headers=self.headers)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content).get('time'), '20:00:00')
        #  проверув 2х словарей (ответ и запрос)
        response = json.loads(response.content)
        for element in self.data:
            # Убрал id пользователя, чтоб не мешался.
            if element != 'user_id':
                self.assertEqual(response[element], self.data[element])
        # проверка работы логики datetime_to_trigger_task
        now = datetime.datetime.now()
        timedelta_now = datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
        resp_hours, rest_minutes, resp_seconds = [int(_) for _ in response['time'].split(':')]
        response_timedelta_time = datetime.timedelta(hours=resp_hours, minutes=rest_minutes, seconds=resp_seconds)
        if timedelta_now > response_timedelta_time:
            to_be_time = now.replace(hour=0, minute=0, second=0,
                                     tzinfo=pytz.timezone(TIME_ZONE)) + response_timedelta_time + datetime.timedelta(
                days=1)
        else:
            to_be_time = (now.replace(microsecond=0, hour=0, minute=0, second=0,
                                      tzinfo=pytz.timezone(TIME_ZONE)) + response_timedelta_time)
        self.assertEqual(str(to_be_time).split('.')[0],
                         response['datetime_to_trigger_task'].split('.')[0].replace('T', ' '))

    def test_update_habit(self):
        """Тестирование изменения привычки.
        Меняем время с 20:00:00 на 18:00:00"""
        changed_data = {
            "time": "18:00:00"
        }
        habit_url = reverse_lazy('habits:habit-detail', args=[self.habit.id])
        response = self.client.patch(path=habit_url, format='json', data=changed_data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['time'], changed_data['time'])

    def test_list_habit(self):
        """Тестирование списка привычек присущие только одному пользователю"""

        # Создаем нового пользователя
        client_list = APIClient()

        #   Авторизация user

        access_token = client_list.post(self.auth_url, {
            'username': self.user_date_2.get('username'),
            'password': self.user_date_2.get('password')
        }).data.get('access')
        client_list.credentials(HTTP_AUTHORIZATION=f'Token {access_token}')
        headers = {
            'Authorization': f'Token {access_token}',
            'Content-Type': 'application/json'
        }
        #  Разные данные пользователей для 2х привычек
        data = self.data.copy()
        data['user_id'] = self.user_2.id
        Habit.objects.create(**data)
        Habit.objects.create(**data)
        #  Запрос HTTP
        habit_url = reverse('habits:habit-list')
        response = client_list.get(path=habit_url, format='json', headers=headers)
        #  Проверяем что привычки присутствуют только у user_2, потому что в headers данные пользователя 2
        for _ in response.data['results']:
            self.assertTrue(_['user'] == self.user_2.id)
        self.assertTrue(isinstance(json.loads(response.content), dict))

    def test_delete_habit(self):
        """Тестирование удаления привычки"""
        created_habit_1 = Habit.objects.create(**self.data)
        habit_url = reverse_lazy('habits:habit-detail', args=[created_habit_1.id])
        response = self.client.delete(path=habit_url, format='json', headers=self.headers)
        self.assertTrue(bool(created_habit_1))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_all_habits(self):
        """Тестирование списках всех привычек у пользователей"""
        data_1 = self.data.copy()
        data_1.update({'user_id': self.user_2.id})
        Habit.objects.create(**data_1)
        Habit.objects.create(**self.data)
        habit_url = reverse('habits:habit-list')
        response = self.client.get(path=habit_url, format='json', headers=self.headers)
        # Проверка, поскольку в экземпляре класса теста стоит по умолчанию авторизация self.user (см. setUp), то и
        #  привычки будут только self.user
        for _ in response.data['results']:
            self.assertEqual(_['user'], self.user.id)
