from django.conf import settings
from django.db import models
from college.models import Department, CustomPerson
from django.urls import reverse


class Profession(models.Model):

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'
        ordering = ('name',)

    number = models.CharField(max_length=20, verbose_name='Код', help_text='Номер специальности. Пример: "09.02.07"')
    name = models.CharField(max_length=70, verbose_name='Наименование', db_index=True, help_text='Полное наименование специальности. Пример: "Информационные системы и программирование"')
    shortname = models.CharField(max_length=25, verbose_name='Идентификатор учебных групп', help_text='Префикс используемый в названиях учебных групп. Пример: "ИСиП", "СИТ')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name='Площадка', help_text='Основная площадка', related_name='profession_department_to_department_id_fkey')

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


class Studygroup(models.Model):

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('name',)

    name = models.CharField(max_length=75, verbose_name='Название', help_text='Например: ИСиП-15', unique=True)
    slug = models.SlugField(verbose_name='URL', max_length=95, db_index=True, unique=True)
    admin_name = models.CharField(max_length=75, verbose_name='Служебное имя', help_text='Имя в ActiveDirectory',
                                  unique=True, null=True, blank=True)
    start_edu = models.DateField(verbose_name='Начало обучения', blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name='Площадка', blank=True, null=True,
                                   related_name='studygroup_department_to_department_id_fkey')
    profession = models.ForeignKey(Profession, on_delete=models.PROTECT, verbose_name='Специальность',
                                   related_name='studygroup_profession_to_profession_id_fkey')
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Куратор',
                                   blank=True, null=True, related_name='studygroup_supervisor_to_customperson_id_fkey')
    assistant = models.ForeignKey(CustomPerson, on_delete=models.PROTECT, verbose_name='Староста', blank=True,
                                  null=True, related_name='studygroup_assistant_to_customuser_id_fkey')

    def __str__(self):
        return f'{self.name}'
