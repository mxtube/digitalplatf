from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from core.storage import get_media_upload_path
from phonenumber_field.modelfields import PhoneNumberField


class CustomPerson(AbstractUser):
    """ Extension for basic user model """
    userpic = models.ImageField(upload_to='img/userpic/', verbose_name='Изображение', blank=True, null=True)
    ldap_userpic = models.BinaryField(verbose_name='Изображение LDAP', null=True, blank=True)
    middle_name = models.CharField(max_length=50, verbose_name='Отчество', blank=True)
    mobile = PhoneNumberField(verbose_name='Мобильный телефон', region='', blank=True, null=True)
    birthday = models.DateField(max_length=10, blank=True, null=True, verbose_name='Дата рождения')
    note = models.TextField(max_length=200, verbose_name='Примечание', blank=True)
    job_title = models.TextField(verbose_name='Должность', blank=True)
    alternative_email = models.EmailField(blank=True, verbose_name='Альтернативный адрес электронной почты')
    is_teacher = models.BooleanField(verbose_name='Преподаватель', default=False)
    group = models.ForeignKey('educationpart.Studygroup', on_delete=models.PROTECT, verbose_name='Учебная группа',
                              related_name='user_group_to_studygroup_id_fkey', null=True, blank=True)

    def __repr__(self):
        return f'{self.__class__}: {self.pk} {self.username}'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    @property
    @admin.display(description="ФИО")
    def get_fullname(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def get_name_initials(self):
        if not self.middle_name:
            return f'{self.last_name} {self.first_name[0]}.'
        return f'{self.last_name} {self.first_name[0]}.{self.middle_name[0]}.'

    def get_user_professional(self):
        return f'{self.group.profession.number} {self.group.profession.name}'

    def get_user_department(self):
        return f'{self.group.department}'

    def get_user_supervisor(self):
        return f'{self.group.supervisor}'

    @staticmethod
    def get_user_by_fio(fio: str):
        try:
            value = fio.split()
            if len(value) == 2:
                return CustomPerson.objects.get(first_name=value[1], last_name=value[0])
            elif len(value) == 3:
                return CustomPerson.objects.get(first_name=value[1], last_name=value[0], middle_name=value[2])
            else:
                return None
        except CustomPerson.DoesNotExist:
            return None
