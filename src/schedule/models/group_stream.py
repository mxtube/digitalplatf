from django.db import models
from educationpart.models import Studygroup
from .stream import Stream


class GroupStream(models.Model):

    class Meta:
        verbose_name = 'Распределение групп потока'
        verbose_name_plural = 'Распределение групп потоков'
        ordering = ('stream',)

    group = models.ForeignKey(Studygroup, on_delete=models.PROTECT, verbose_name='Группа', null=True,
                              related_name='groupstream_group_to_studygroup_id_fkey')
    stream = models.ForeignKey(Stream, on_delete=models.PROTECT, verbose_name='Поток', null=True,
                               related_name='groupstream_stream_to_stream_id_fkey')

    def __repr__(self):
        return f'{self.__class__}: {self.pk} {self.group} {self.stream}'

    def __str__(self):
        return f'{self.stream} {self.group}'
