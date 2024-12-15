from django.db import models
from educationpart.models import Studygroup
from .schedule_calendar_mark import ScheduleCalendarMark


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
