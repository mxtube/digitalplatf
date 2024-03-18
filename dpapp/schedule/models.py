from django.urls import reverse
from django.db import models
from educationpart.models import Studygroup, Discipline
from college.models import Department, Auditory, CustomPerson
from datetime import datetime, timedelta


class NumberWeek(models.Model):

    name = models.CharField(max_length=15, unique=True)

    def __repr__(self):
        return f'{self.__class__}: {self.pk} {self.name}'

    def __str__(self):
        return f'{self.name}'


class DayWeek(models.Model):

    name = models.CharField(max_length=15)
    week = models.ForeignKey(NumberWeek, on_delete=models.PROTECT, related_name='dayweek_week_to_numberweek_id_fkey')

    def __repr__(self):
        return f'{self.__class__}: {self.pk} {self.name} {self.week}'

    def __str__(self):
        return f'{self.name} {self.week}'


class Stream(models.Model):

    class Meta:
        verbose_name = 'Распределение групп потоков - обозначения'
        verbose_name_plural = 'Распределение групп потоков - обозначения'
        ordering = ('number',)

    number = models.CharField(max_length=30, verbose_name='Наименование', help_text='Например: 1 поток')

    def __repr__(self):
        return f'{self.__class__}: {self.pk} {self.number}'

    def __str__(self):
        return f'{self.number}'


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


class ScheduleCalendarMark(models.Model):

    class Meta:

        verbose_name = 'График учебного процесса - обозначения'
        verbose_name_plural = 'График учебного процесса - обозначения'
        ordering = ('name',)

    name = models.CharField(max_length=100, verbose_name='Наименование', unique=True)
    symbol = models.CharField(max_length=5, verbose_name='Символ', help_text='Символ отображаемый в графике',
                              blank=True, null=True, unique=True)

    def __repr__(self):
        return f'{self.__class__}: {self.pk} {self.name} {self.symbol}'

    def __str__(self):
        return f'{self.symbol} {self.name}'


class ScheduleCalendar(models.Model):

    class Meta:

        verbose_name = 'График учебного процесса'
        verbose_name_plural = 'График учебного процесса'

    start_week = models.DateField(verbose_name='Начало учебной недели')
    end_week = models.DateField(verbose_name='Конец учебной недели')
    group = models.ForeignKey(Studygroup, verbose_name='Группа', on_delete=models.PROTECT,
                              related_name='schcal_group_to_studygroup_id_fkey')
    mark = models.ForeignKey(ScheduleCalendarMark, verbose_name='Отметка', on_delete=models.PROTECT,
                             related_name='schcal_mark_to_schcalmark_id_fkey')

    def __str__(self):
        return f'{self.group} {self.start_week} {self.end_week} {self.mark}'


class Schedule(models.Model):

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'
        ordering = ('date',)

    date = models.DateField(verbose_name='Дата', db_index=True)
    couple = models.ForeignKey(Couple, verbose_name='Номер пары', on_delete=models.PROTECT,
                               related_name='chgsched_couple_to_couple_id_fkey')
    group = models.ForeignKey(Studygroup, verbose_name='Группа', on_delete=models.PROTECT, db_index=True,
                              related_name='chgsched_studygroup_to_studygroup_id_fkey')
    auditory = models.ForeignKey(Auditory, verbose_name='Аудитория', on_delete=models.PROTECT,
                                 related_name='chgsched_auditory_to_auditory_id_fkey')
    discipline = models.ForeignKey(Discipline, verbose_name='Дисциплина', on_delete=models.PROTECT,
                                   related_name='chgsched_discipline_to_discipline_id_fkey')
    teacher = models.ForeignKey(CustomPerson, verbose_name='Преподаватель', on_delete=models.PROTECT,
                                related_name='chgsched_teacher_to_customperson_id_fkey')

    def __str__(self):
        return f'{self.date} {self.group} {self.couple} {self.auditory} {self.discipline} {self.teacher}'

    def get_absolute_url(self):
        return reverse('schedule_detail_group', kwargs={
            'department_name': self.group.department.slug,
            'group': self.group.slug,
            'date': self.date
        })

    @staticmethod
    def _number_week(date: datetime.date) -> str:
        """ Метод получения четности недели """
        return 'Четная' if date.isocalendar()[1] % 2 == 0 else 'Нечетная'

    @classmethod
    def has_data_by_date(cls, date) -> bool:
        return cls.objects.filter(date=date).exists()

    @classmethod
    def has_date_by_range(cls, start_date: str, end_date: str, day: str):
        dates = Schedule.get_date_by_range(start_date, end_date, day)
        return cls.objects.filter(date__in=dates).exists()

    @staticmethod
    def get_date_by_range(start_date: str, end_date: str, week_day: str):
        dates = []
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        current_date = start_date
        while current_date <= end_date:
            if week_day.split()[1] == 'Еженедельно':
                if current_date.strftime('%A').capitalize() == week_day.split()[0]:
                    dates.append(current_date.strftime('%Y-%m-%d'))
            else:
                if current_date.strftime('%A').capitalize() == week_day.split()[0]:
                    if Schedule._number_week(current_date) == week_day.split()[1]:
                        dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
        return dates


class UploadSchedules(models.Model):

    class Meta:
        verbose_name = 'Загрузить расписание'
        verbose_name_plural = 'Загрузить расписание'


class DashboardSchedule(models.Model):

    class Meta:
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboard'
