from django.db import models
from college.models import Department

class Profession(models.Model):

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'
        ordering = ('name',)

    number = models.CharField(max_length=20, verbose_name='Код', help_text='Номер специальности. Пример: "09.02.07"')
    name = models.CharField(max_length=70, verbose_name='Наименование', db_index=True, help_text='Полное наименование специальности. Пример: "Информационные системы и программирование"')
    shortname = models.CharField(max_length=25, verbose_name='Идентификатор учебных групп', help_text='Префикс используемый в названиях учебных групп. Пример: "ИСиП", "СИТ')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name='Площадка', help_text='Основная площадка')

    def __str__(self):
        return f'{self.number} {self.name}'


class Discipline(models.Model):

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
        ordering = ('name',)

    name = models.CharField(max_length=150, verbose_name='Наименование', help_text='Введите название дисциплины. Пример: "Разработка веб-сайтов".', unique=True)

    def __str__(self):
        return f'{self.name}'