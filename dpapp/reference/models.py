from django.db import models


class Status(models.Model):

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = "Статусы"

    name = models.CharField(max_length=50, unique=True, verbose_name='Название', help_text='Наименование статуса')
    # TODO: Добавить поле цвет, для окращивания строк в таблице "Справки". Можно использовать библиотеку django-colorfield (https://pypi.org/project/django-colorfield/)

    def __str__(self):
        return f'{self.name}'