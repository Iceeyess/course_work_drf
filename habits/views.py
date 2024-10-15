from django.shortcuts import render
from rest_framework import viewsets

from habits.models import Habit
from habits.serializers import HabitSerializer


# Create your views here.


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer