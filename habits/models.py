from django.db import models

from users.models import User

NULLABLE = dict(null=True, blank=True)

# Create your models here.
class Habit(models.Model):
    """Модель привычки.
    Заметки:
    - place: место, в котором выполняется привычка.
    - time: время, когда выполняется привычка.
    - activity: действие, которое представляет собой привычка.
    - is_pleasant_sign: признак приятной привычки. True/False признак является ли поле ссылкой для полезной привычки.
    По умолчанию поле False, однако, если создается признак приятной привычки(ставится True), то это экземпляр класса
    можно использовать как продолжение полезной привычки.
    - related_habit: связанная привычка. Если заполнено это поле, то не может быть True у pleasant_sign или выбрано
    award. Не для приятных привычек. Если поле related_habit заполнено, то is_pleasant_sign будет False, если
    related_habit будет пусто, значит поле is_pleasant_sign будет True.
    - regularity: периодичность выполнения привычки.
    - award: вознаграждение. Может быть заполнено только, или поле award, или поле pleasant_sign, поскольку одновременно
    нельзя иметь признак приятной привычки или вознаграждение.
     - time_spent: потраченное время на выполнение привычки.
     - is_public: признак публичности. Привычки можно публиковать в общий доступ, чтобы другие пользователи могли брать
     в пример чужие привычки """
    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE)
    place = models.CharField(max_length=200, verbose_name='место', help_text='место, в котором выполняется привычка')
    time = models.TimeField(verbose_name='время', help_text='время, когда выполняется привычка')
    activity = models.CharField(max_length=500, verbose_name='действие',
                                help_text='действия, которое представляет собой привычка')
    is_pleasant_sign = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='связанная привычка',
                                      **NULLABLE)
    regularity = models.CharField(default='ежедневная', max_length=200, verbose_name='периодичность')
    award = models.CharField(max_length=500, verbose_name='вознаграждение', **NULLABLE)
    time_spent = models.DurationField(verbose_name='потраченное время',
                                      help_text='потраченное время на выполнение привычки',
                                      **NULLABLE)
    is_public = models.BooleanField(verbose_name='признак публичности')

    def __repr__(self):
        return f"Модель привычек №{self.id}"

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
        ordering = ('pk', )