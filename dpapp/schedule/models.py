from django.db import models
from educationpart.models import Studygroup

class Stream(models.Model):

    class Meta:
        verbose_name = 'Поток'
        verbose_name_plural = 'Потоки'
        ordering = ('number',)

    number = models.CharField(max_length=30, verbose_name='Наименование потока', help_text='Пример: "1 поток", "2 поток"')


class GroupStream(models.Model):

    class Meta:
        verbose_name = 'Распределение потока'
        verbose_name_plural = 'Распределение потоков'
        ordering = ('stream',)

    group = models.ForeignKey(Studygroup, on_delete=models.PROTECT, verbose_name='Группа', null=True, related_name='groupstream_group_to_studygroup_id_fkey')
    stream = models.ForeignKey(Stream, on_delete=models.PROTECT, verbose_name='Поток', null=True, related_name='groupstream_stream_to_stream_id_fkey')