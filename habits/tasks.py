from datetime import datetime, timedelta, timezone, tzinfo
import pytz

from celery import shared_task
from .services import send_tg_message
from habits.models import Habit
from config.settings import TG_CHAT_ID, TIME_ZONE

@shared_task
def check_time_to_trigger_habit() -> None:
    """Функция-задача, которая выполняет отправку, если текущее время подошло к запуску и увеличивает интервал для
    следующего запуска. Должна быть настроена на 1-10 ежеминутные запуски, в идеале"""
    now = datetime.now().replace(tzinfo=pytz.timezone(TIME_ZONE))
    habits_list = Habit.objects.all()
    for habit in habits_list:
        if habit.datetime_to_trigger_task:
            # datetime_to_trigger_task = datetime.strptime(str(habit.datetime_to_trigger_task),'%Y-%m-%d %H:%M:%S.%f%z')
            datetime_to_trigger_task = habit.datetime_to_trigger_task.astimezone(pytz.timezone(TIME_ZONE))
            if habit.datetime_to_trigger_task and now > datetime_to_trigger_task:
                print(datetime_to_trigger_task)
                message = f'я буду {habit.activity} в {habit.time} в {habit.place}'
                send_tg_message(TG_CHAT_ID, message)
                habit.datetime_to_trigger_task += timedelta(days=int(habit.regularity))  # прибавляем период к следующему запуску
                habit.save()
