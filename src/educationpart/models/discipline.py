from django.db import models


class Discipline(models.Model):

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
        ordering = ('name',)

    name = models.CharField(
        max_length=150,
        verbose_name='Наименование',
        help_text='Введите название дисциплины. Пример: "Разработка веб-сайтов".',
        unique=True
    )

    def __str__(self):
        return f'{self.name}'
