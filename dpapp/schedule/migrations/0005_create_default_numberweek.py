# Generated by Django 5.0 on 2023-12-30 08:31

from django.db import migrations
from schedule.models import NumberWeek


class Migration(migrations.Migration):

    dependencies = [('schedule', '0004_numberweek'),]

    def create_week_number(apps, schema_editor):

        objs = NumberWeek.objects.bulk_create(
            [
                NumberWeek(id=1, name='Четная'),
                NumberWeek(id=2, name='Нечетная')
            ]
        )

    operations = [migrations.RunPython(create_week_number),]
