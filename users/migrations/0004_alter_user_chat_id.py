# Generated by Django 5.1.2 on 2024-10-21 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_chat_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='chat_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='CHAT ID от телеграмма'),
        ),
    ]