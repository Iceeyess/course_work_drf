from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import permission_classes, api_view

from habits.models import Habit
from habits.serializers import HabitSerializer
from .pagination import FiveHabitsOnPage
from .permissions import IsHabitOwner, IsReadOnly

# Create your views here.


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsHabitOwner | IsReadOnly, ]
    pagination_class = FiveHabitsOnPage

    def create(self, request, *args, **kwargs):
        """Сохраняет текущего пользователя в модель БД"""
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)

    def get(self, request):
        queryset = Habit.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = HabitSerializer(FiveHabitsOnPage, many=True)
        return self.get_paginated_response(serializer.data)