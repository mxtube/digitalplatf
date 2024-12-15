from django.db import models


class NumberWeek(models.Model):

    name = models.CharField(max_length=15, unique=True)

    def __repr__(self):
        return f'{self.__class__}: {self.pk} {self.name}'

    def __str__(self):
        return f'{self.name}'
