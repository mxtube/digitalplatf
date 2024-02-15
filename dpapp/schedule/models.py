from django.db import models
from educationpart.models import Studygroup
from college.models import Department


class NumberWeek(models.Model):

    name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f'{self.name}'


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


class Couple(models.Model):

    class Meta:
        verbose_name = 'Звонок'
        verbose_name_plural = 'Расписание звонков'
        ordering = ('stream',)

    stream = models.ForeignKey('Stream', on_delete=models.PROTECT, verbose_name='Поток', related_name='couple_stream_to_stream_id_fkey')
    number = models.CharField(max_length=200, verbose_name='Номер пары', help_text='Пример: "1 пара", "2 пара"')
    time_start = models.TimeField(verbose_name='Начало', help_text='Время начала урока')
    time_end = models.TimeField(verbose_name='Конец', help_text='Время окончания урока')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name='Площадка', blank=True, null=True, related_name='couple_department_to_department_id_fkey')

    def __repr__(self):
        return f'{self.__class__}: {self.pk} {self.number} - {self.stream}'

    def __str__(self):
        return f'{self.number}'