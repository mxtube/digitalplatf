from django.db import models


class Status(models.Model):

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = "Статусы"

    name = models.CharField(max_length=50, unique=True, verbose_name='Название', help_text='Наименование статуса')
    # TODO: Добавить поле цвет, для окращивания строк в таблице "Справки". Можно использовать библиотеку django-colorfield (https://pypi.org/project/django-colorfield/)

    def __str__(self):
        return f'{self.name}'


class Type(models.Model):

    class Meta:
        verbose_name = 'Тип справки'
        verbose_name_plural = 'Типы справок'

    name = models.CharField(max_length=100, unique=True, verbose_name='Наименование')
    example = models.FileField(upload_to='reference/example', verbose_name='Образец справки')

    def __repr__(self):
        return f'{self.__class__}: {self.name}'

    def __str__(self):
        return f'{self.name}'