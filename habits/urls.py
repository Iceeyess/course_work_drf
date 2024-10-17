from django.urls import path
from rest_framework import routers

from habits.apps import HabitsConfig
from habits.views import HabitViewSet, GetAllHabits

app_name = HabitsConfig.name

router = routers.DefaultRouter()
router.register(f'habits', HabitViewSet, basename='habit')

urlpatterns = [
    path('habits/all/', GetAllHabits.as_view(), name='all-ahbits'),
]
urlpatterns += router.urls