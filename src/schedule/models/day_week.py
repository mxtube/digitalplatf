from django.db import models


class DayWeek(models.Model):

    name = models.CharField(max_length=15)
    week = models.ForeignKey('NumberWeek', on_delete=models.PROTECT, related_name='dayweek_week_to_numberweek_id_fkey')

    def __repr__(self):
        return f'{self.__class__}: {self.pk} {self.name} {self.week}'

    def __str__(self):
        return f'{self.name} {self.week}'
