from django.db import models
from django.urls import reverse
from datetime import datetime, timedelta
from college.models import CustomPerson, Auditory
from educationpart.models import Studygroup, Discipline
from .couple import Couple


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

    def get_absolute_url_group(self):
        return reverse('schedule_group', kwargs={
            'department_name': self.group.department.slug,
            'group': self.group.slug,
            'date': self.date
        })

    def get_absolute_url_teacher(self):
        return reverse('schedule_teacher', kwargs={
            'department_name': self.group.department.slug,
            'teacher': self.teacher.id,
            'date': self.date.strftime('%Y-%m-%d')
        })

    def get_absolute_url_all(self):
        return reverse('schedule_dpt', kwargs={
            'department_name': self.group.department.slug,
            'date': self.date.strftime('%Y-%m-%d')
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
