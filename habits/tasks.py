from datetime import datetime, timedelta
import pytz

from celery import shared_task
from .services import send_tg_message
from habits.models import Habit
from config.settings import TIME_ZONE


@shared_task
def check_time_to_trigger_habit() -> None:
    """Функция-задача, которая выполняет отправку, если текущее время подошло к запуску и увеличивает интервал для
    следующего запуска. Должна быть настроена на 1-10 ежеминутные запуски, в идеале"""
    now = datetime.now(pytz.timezone(TIME_ZONE))
    habits_list = Habit.objects.all()
    for habit in habits_list:
        if habit.datetime_to_trigger_task:
            datetime_to_trigger_task = habit.datetime_to_trigger_task.astimezone(pytz.timezone(TIME_ZONE))
            if habit.datetime_to_trigger_task and now > datetime_to_trigger_task:
                if habit.user.chat_id:
                    #  Если в БД есть chat_id от  Телеграмма, то вызовет функцию send_tg_message
                    #  и обновит поле datetime_to_trigger_task
                    message = f'я буду {habit.activity} в {habit.time} в {habit.place}'
                    send_tg_message(habit.user.chat_id, message)
                    habit.datetime_to_trigger_task += timedelta(days=int(habit.regularity))  # прибавляем период
                    habit.save()
                else:
                    #  Если в БД нет chat_id, то в консоли будет предупреждение, дальнейшая логика с БД
                    #  не будет работать, пока не обновит свои данные.
                    print(f'У пользователя {habit.user} нет чата в Telegram. Обновите поле chat_id.')
