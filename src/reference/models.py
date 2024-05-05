import uuid
from django.db import models
from college.models import CustomPerson

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


class Reference(models.Model):

    class Meta:
        verbose_name = 'Справка'
        verbose_name_plural = 'Справки'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomPerson, on_delete=models.PROTECT, verbose_name='Заявитель', related_name='reference_user_to_customperson_id_fkey')
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name='Тип справки', related_name='reference_type_to_type_id_fkey')
    comment = models.TextField(max_length=500, null=True, blank=True, verbose_name='Примечание')
    reference_count = models.IntegerField(default=1, verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, default=1, verbose_name='Статус', related_name='reference_status_to_status_id_fkey')

    def __repr__(self):
        return f'{self.__class__}: {self.id}'

    def __str__(self):
        return f'{self.id}'