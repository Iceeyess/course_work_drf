from django.urls import path
from rest_framework import routers

from habits.apps import HabitsConfig
from habits.views import HabitViewSet, GetAllHabits

app_name = HabitsConfig.name

router = routers.DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')

urlpatterns = [
    # все привычки всех пользователей
    path('habits/all/', GetAllHabits.as_view(), name='all-habits'),
]
urlpatterns += router.urls
