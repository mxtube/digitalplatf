# Generated by Django 5.0.1 on 2024-02-09 20:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educationpart', '0003_studygroup'),
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupStream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                            related_name='groupstream_group_to_studygroup_id_fkey',
                                            to='educationpart.studygroup', verbose_name='Группа')),
                ('stream', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                             related_name='groupstream_stream_to_stream_id_fkey', to='schedule.stream',
                                             verbose_name='Поток')),
            ],
            options={
                'verbose_name': 'Распределение групп потока',
                'verbose_name_plural': 'Распределение групп потоков',
                'ordering': ('stream',),
            },
        ),
    ]
