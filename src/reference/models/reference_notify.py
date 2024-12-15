from typing import List

from django.db import models
from college.models import Department


class ReferenceNotify(models.Model):

    class Meta:
        verbose_name = 'Оповещение'
        verbose_name_plural = 'Настройка оповещений'

    email = models.EmailField(verbose_name='Электронная почта', null=False)
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        verbose_name='Площадка',
        related_name='reference_notify_to_department_id_fkey'
    )

    def __repr__(self):
        return f'{self.__class__}: {self.id}'

    def __str__(self):
        return f'{self.id}: {self.department} {self.email}'

    @staticmethod
    def get_emails_by_department(department: Department) -> List:
        return ReferenceNotify.objects.filter(department=department).values_list('email', flat=True)
