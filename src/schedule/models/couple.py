from django.db import models
from .stream import Stream
from college.models import Department


class Couple(models.Model):

    class Meta:
        verbose_name = 'Звонок'
        verbose_name_plural = 'Расписание звонков'
        ordering = ('stream',)

    stream = models.ForeignKey(Stream, on_delete=models.PROTECT, verbose_name='Поток',
                               related_name='couple_stream_to_stream_id_fkey')
    number = models.CharField(max_length=200, verbose_name='Номер пары', help_text='Например: 1 пара')
    time_start = models.TimeField(verbose_name='Начало', help_text='Время начала урока')
    time_end = models.TimeField(verbose_name='Конец', help_text='Время окончания урока')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name='Площадка', blank=True, null=True,
                                   related_name='couple_department_to_department_id_fkey')

    def __repr__(self):
        return f'{self.__class__}: {self.pk} {self.number} - {self.stream}'

    def __str__(self):
        return f'{self.number}'
