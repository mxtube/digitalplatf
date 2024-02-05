from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomPerson(AbstractUser):
    """ Extension for basic user model """
    middle_name = models.CharField(max_length=50, verbose_name='Отчество', blank=True)
    mobile = models.CharField(validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')], max_length=17, help_text='Введите номер телефона в формате: +999999999', verbose_name='Телефон', blank=True)
    birthday = models.DateField(max_length=10, blank=True, null=True, verbose_name='Дата рождения')
    note = models.TextField(max_length=200, verbose_name='Примечание', blank=True)
    alternative_email = models.EmailField(blank=True, verbose_name='Альтернативный адрес электронной почты')

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'