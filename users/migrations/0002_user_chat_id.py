# Generated by Django 5.1.2 on 2024-10-18 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='chat_id',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='CHAT ID от тел'),
        ),
    ]
