from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from django.urls import reverse


class Department(models.Model):

    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'
        ordering = ('short_name',)

    name = models.CharField(max_length=200, verbose_name='Наименование', help_text='Полное наименование')
    slug = models.SlugField(verbose_name='URL', max_length=200, db_index=True, unique=True)
    short_name = models.CharField(max_length=50, verbose_name='Сокращение', help_text='Сокращенное название')
    phone = models.CharField(validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')], max_length=17, blank=True,
                             verbose_name='Телефон', help_text='Введите номер телефона в формате: +999999999')
    email = models.EmailField(blank=True, verbose_name='Адрес электронной почты')
    coordinate = models.CharField(max_length=500, verbose_name='Адрес', help_text='Введите адрес расположения площадки',
                                  blank=True)
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Руководитель',
                                   null=True, blank=True, related_name='department_supervisor_to_customperson_id_fkey')

    def __repr__(self):
        return f'{self.__class__}: {self.pk} {self.name}'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('schedule_home', kwargs={'department_name': self.slug})
