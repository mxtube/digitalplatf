from django.conf import settings
from django.db import models
from college.models import Department, CustomPerson


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
    profession = models.ForeignKey('Profession', on_delete=models.PROTECT, verbose_name='Специальность',
                                   related_name='studygroup_profession_to_profession_id_fkey')
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Куратор',
                                   blank=True, null=True, related_name='studygroup_supervisor_to_customperson_id_fkey')
    assistant = models.ForeignKey(CustomPerson, on_delete=models.PROTECT, verbose_name='Староста', blank=True,
                                  null=True, related_name='studygroup_assistant_to_customuser_id_fkey')

    def __str__(self):
        return f'{self.name}'
