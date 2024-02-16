import datetime

from django.db import models
from educationpart.models import Studygroup
from college.models import Department


class NumberWeek(models.Model):

    name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f'{self.name}'


class DayWeek(models.Model):

    name = models.CharField(max_length=15)
    week = models.ForeignKey(NumberWeek, on_delete=models.PROTECT, related_name='dayweek_week_to_numberweek_id_fkey')

    def __str__(self):
        return f'{self.name}'


class Stream(models.Model):

    class Meta:
        verbose_name = 'Поток'
        verbose_name_plural = 'Потоки'
        ordering = ('number',)

    number = models.CharField(max_length=30, verbose_name='Наименование потока', help_text='Пример: "1 поток", "2 поток"')

    def __str__(self):
        return f'{self.number}'


class GroupStream(models.Model):

    class Meta:
        verbose_name = 'Распределение потока'
        verbose_name_plural = 'Распределение потоков'
        ordering = ('stream',)

    group = models.ForeignKey(Studygroup, on_delete=models.PROTECT, verbose_name='Группа', null=True, related_name='groupstream_group_to_studygroup_id_fkey')
    stream = models.ForeignKey(Stream, on_delete=models.PROTECT, verbose_name='Поток', null=True, related_name='groupstream_stream_to_stream_id_fkey')

    def __str__(self):
        return f'{self.stream} {self.group}'


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


class ScheduleCalendarMark(models.Model):

    class Meta:

        verbose_name = 'Обозначение календарного графика'
        verbose_name_plural = 'Обозначения календарного графика'
        ordering = ('name',)

    name = models.CharField(max_length=100, verbose_name='Наименование', unique=True)
    symbol = models.CharField(max_length=5, verbose_name='Символ', help_text='Символ отображаемый в графике', blank=True, null=True, unique=True)

    def __str__(self):
        return f'{self.symbol} {self.name}'


class ScheduleCalendar(models.Model):

    class Meta:

        verbose_name = 'График учебного процесса'
        verbose_name_plural = 'График учебного процесса'

    start_week = models.DateField(verbose_name='Начало учебной недели')
    end_week = models.DateField(verbose_name='Конец учебной недели')
    group = models.ForeignKey(Studygroup, verbose_name='Группа', on_delete=models.PROTECT, related_name='schcal_group_to_studygroup_id_fkey')
    mark = models.ForeignKey(ScheduleCalendarMark, verbose_name='Отметка', on_delete=models.PROTECT, related_name='schcal_mark_to_schcalmark_id_fkey')

    def __str__(self):
        return f'{self.group} {self.start_week} {self.end_week} {self.mark}'

