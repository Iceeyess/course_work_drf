from rest_framework import serializers

from habits.models import Habit
from habits.validators import CheckRelatedHabitAgainstAward, TimeSpentValidation, IsPleasantSignTrueForRelatedHabit, \
    PeriodLimitValidation


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            CheckRelatedHabitAgainstAward(field='related_habit'), TimeSpentValidation(field='time_spent'),
            IsPleasantSignTrueForRelatedHabit(field='related_habit'), PeriodLimitValidation(field='regularity')
        ]
