from django.contrib import admin
from habits.models import Habit


# Register your models here.
admin.site.register(Habit)


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'activity', 'is_pleasant_sign', 'related_habit', 'time_spent',
                    'datetime_to_trigger_task', 'is_public', )
    list_filter = ('is_public', )
    search_fields = ('id', 'activity', )
