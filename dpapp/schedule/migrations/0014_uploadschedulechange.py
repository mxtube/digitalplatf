# Generated by Django 5.0.1 on 2024-02-23 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0013_uploadschedulebase'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadScheduleChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Загрузить изменение в расписание',
                'verbose_name_plural': 'Загрузить изменение в расписание',
            },
        ),
    ]
