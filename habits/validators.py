import datetime

from rest_framework import serializers


class CheckRelatedHabitAgainstAward:
    """Класс проверки значений полей related_habit и award"""

    def __init__(self,field):
        self.field = field

    def __call__(self,value):
        """Проверка значений полей related_habit и award
        Если related_habit указан и award, то вызывается исключение. Кроме того делается доп. проверка на то,
        что, если это приятная привычка, то у нее не может быть заполнено поле related_habit или award"""
        field1, field2 = 'related_habit', 'award'
        related_habit, award = value.get(field1), value.get(field2)
        if related_habit and award:
            raise serializers.ValidationError(f'Нельзя указать одновременно указать {field1} и {field2}.')
        if value.get('is_pleasant_sign'):
            if related_habit or award:
                raise serializers.ValidationError(f'Нельзя указать {field1} или {field2} при признаке приятной привычки.')

class TimeSpentValidation:
    """Класс валидации поля time_spent"""
    def __init__(self,field):
        self.field = field

    def __call__(self,value):
        """Проверяется поле time_spent, если оно более лимита, то вызывается исключение"""
        limit = datetime.timedelta(minutes=2)
        if value.get('time_spent') > limit:
            raise serializers.ValidationError(f'Потраченное время не может превышать {limit.seconds} секунд.')

class IsPleasantSignTrueForRelatedHabit:
    """Класс проверки поля is_pleasant_sign"""
    def __init__(self,field):
        self.field = field

    def __call__(self,value):
        """Для поля related_habit в объекте может быть только объект, у которого есть признак приятной привычки"""
        related_habit = value.get('related_habit')
        if related_habit:
            if not related_habit.is_pleasant_sign:
                raise serializers.ValidationError(f'Для связанной привычки должен быть признак приятной привычки.')

class PeriodLimitValidation:
    """Класс проверки поля regularity"""
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        """Проверяется поле regularity, если оно более допустимого диапазона, то вызывается исключение"""
        allowed_periods = range(1, 8)  # 1 неделя
        if int(value.get('regularity')) not in allowed_periods:
            raise serializers.ValidationError(f'Периодичность должна быть не более {allowed_periods[-1]} дней.')
