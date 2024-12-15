from django.db import models


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
