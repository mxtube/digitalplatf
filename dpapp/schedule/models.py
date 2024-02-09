from django.db import models


class Stream(models.Model):

    class Meta:
        verbose_name = 'Поток'
        verbose_name_plural = 'Потоки'
        ordering = ('number',)

    number = models.CharField(max_length=30, verbose_name='Наименование потока', help_text='Пример: "1 поток", "2 поток"')