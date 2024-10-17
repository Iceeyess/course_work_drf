from django.shortcuts import render
from rest_framework import viewsets, generics
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

    def list(self, request, *args, **kwargs):
        queryset = Habit.objects.filter(user=request.user)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = HabitSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

class GetAllHabits(generics.ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer