# Generated by Django 5.0.1 on 2024-02-09 08:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0004_auditory'),
        ('educationpart', '0002_discipline'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Studygroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование группы. Пример: "ИСиП-15", "СИТ-115".', max_length=75, unique=True, verbose_name='Наименование')),
                ('admin_name', models.CharField(blank=True, help_text='Имя группы указанное в ActiveDirectory.', max_length=75, null=True, unique=True, verbose_name='Служебное имя')),
                ('start_edu', models.DateField(blank=True, null=True, verbose_name='Начало обучения')),
                ('assistant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='studygroup_assistant_to_customuser_id_fkey', to=settings.AUTH_USER_MODEL, verbose_name='Староста')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='studygroup_department_to_department_id_fkey', to='college.department', verbose_name='Площадка')),
                ('profession', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='studygroup_profession_to_profession_id_fkey', to='educationpart.profession', verbose_name='Специальность')),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='studygroup_supervisor_to_customperson_id_fkey', to=settings.AUTH_USER_MODEL, verbose_name='Куратор')),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
                'ordering': ('name',),
            },
        ),
    ]
