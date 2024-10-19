from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.decorators import permission_classes, api_view

from habits.models import Habit
from habits.serializers import HabitSerializer
from .pagination import FiveHabitsOnPage
from .permissions import IsHabitOwner, IsReadOnly
import datetime


# Create your views here.


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsHabitOwner | IsReadOnly, ]
    pagination_class = FiveHabitsOnPage

    def create(self, request, *args, **kwargs):
        """Сохраняет текущего пользователя в модель БД"""
        request.data['user'] = request.user.id
        # Сохраняем в модель дату и время следующего запуска.
        # Час, минута и секунды переданные в сериализатор
        hour, minute, second = [int(_) for _ in request.data.get('time').split(':')]
        # Создаем формат Timedelta
        time = datetime.timedelta(hours=hour, minutes=minute, seconds=second)
        # Текущее время в формате datetime.datetime
        now_dt = datetime.datetime.now()
        # Текущее время в формате timedelta
        now_timedelta = datetime.timedelta(hours=now_dt.hour, minutes=now_dt.minute, seconds=now_dt.second)
        # Если текущее время больше времени привычки, то откладываем на следующий день
        if now_timedelta > time:
            request.data['datetime_to_trigger_task'] = now_dt.replace(hour=0, minute=0, second=0) + datetime.timedelta(
                days=1) + time
        # В противном случае, делаем в этот день
        else:
            request.data['datetime_to_trigger_task'] = now_dt.replace(hour=0, minute=0, second=0) + time
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """Выдача списка объектов с пагинацией"""
        queryset = Habit.objects.filter(user=request.user)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = HabitSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class GetAllHabits(generics.ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def get_queryset(self):
        """Выдавать только по признаку публичности"""
        return Habit.objects.filter(is_public=True)
