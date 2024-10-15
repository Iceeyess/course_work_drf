from django.urls import path
from rest_framework import routers

from habits.apps import HabitsConfig
from habits.views import HabitViewSet

app_name = HabitsConfig.name

router = routers.DefaultRouter()
router.register(f'habits', HabitViewSet, basename='habit')

urlpatterns = [
]
urlpatterns += router.urls