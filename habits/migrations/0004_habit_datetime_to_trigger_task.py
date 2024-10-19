# Generated by Django 5.1.2 on 2024-10-18 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0003_alter_habit_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='datetime_to_trigger_task',
            field=models.DateTimeField(blank=True, help_text='период следующего запуска напоминания в Телеграмм', null=True, verbose_name='дата и время'),
        ),
    ]