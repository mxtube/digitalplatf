from django.db import models


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
