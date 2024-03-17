# Generated by Django 5.0.1 on 2024-02-16 08:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('schedule', '0004_numberweek'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayWeek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                           related_name='dayweek_week_to_numberweek_id_fkey',
                                           to='schedule.numberweek')),
            ],
        ),
    ]
