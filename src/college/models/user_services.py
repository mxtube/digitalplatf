from django.db import models


class UserServicesCategory(models.Model):

    class Meta:
        verbose_name = 'Категория сервиса'
        verbose_name_plural = 'Сервисы - категории'

    name = models.CharField(max_length=50, verbose_name='Название', unique=True)
    visible = models.BooleanField(verbose_name='Видимость', default=True)

    def __repr__(self):
        return f'{self.__class__}: {self.pk} {self.name}'

    def __str__(self):
        return f'{self.name}'


class UserServices(models.Model):

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'

    category = models.ForeignKey(UserServicesCategory, on_delete=models.PROTECT, verbose_name='Категория',
                                 related_name='usrsrv_cat_to_usrsrvcat_id_fkey', null=True)
    name = models.CharField(max_length=25, verbose_name='Название', unique=True, help_text='Например, СДО Академия')
    link = models.URLField(verbose_name='Ссылка')
    icon = models.CharField(max_length=50, verbose_name='Иконка', help_text='Используйте Fontawesome')
    visible = models.BooleanField(verbose_name='Видимость', default=True)

    def __repr__(self):
        return f'{self.__class__}: {self.pk} {self.name}'

    def __str__(self):
        return f'{self.name}'
