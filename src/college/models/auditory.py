from django.db import models


class Auditory(models.Model):

    class Meta:
        verbose_name = 'Аудитория'
        verbose_name_plural = 'Аудитории'
        ordering = ('number',)
        unique_together = ('number', 'department')

    number = models.CharField(max_length=20, help_text='Номер аудитории', verbose_name='Номер')
    department = models.ForeignKey(
        'Department',
        on_delete=models.PROTECT,
        default=None,
        verbose_name='Площадка',
        related_name='auditory_department_to_department_id_fkey'
    )

    def __repr__(self):
        return f'{self.__class__}: {self.pk} {self.department} {self.number}'

    def __str__(self):
        return f'{self.number}'
