from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib import admin
from django.urls import reverse


class SingletonModel(models.Model):
    """
    https://evileg.com/en/post/576/#header_SingletonModel
    """
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class SiteSettings(SingletonModel):

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'

    site_name = models.CharField(verbose_name='Полное название сайта', max_length=256, default='Цифровая платформа')
    short_site_name = models.CharField(verbose_name='Краткое название сайта', max_length=19, help_text='Например, одним словом')
    logotype = models.ImageField(verbose_name='Логотип', upload_to='site/img', name='logotype', blank=True, null=True)
    description = models.TextField(verbose_name='Описание главной страницы')

    # Contacts
    contact_description = models.CharField(verbose_name='Контактная информация', help_text='Дополнительная контактная информация. Отображается под заголовком.', max_length=100, blank=True, null=True)
    phone = models.CharField(validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')], verbose_name='Телефон', help_text='Номер телефона в формате: +999999999', max_length=17, blank=True, null=True)
    email = models.EmailField(verbose_name='Электронная почта', help_text='Пример: example@mail.ru', blank=True, null=True)
    address = models.CharField(verbose_name='Адрес', help_text='Пример: 129344, г. Москва, Проспект мира д.1', max_length=100, blank=True, null=True)

    # Social Network
    vk_link = models.URLField(verbose_name='Вконтакте', blank=True, null=True)
    youtube_link = models.URLField(verbose_name='YouTube', blank=True, null=True)
    odnoklassniki_link = models.URLField(verbose_name='Одноклассники', blank=True, null=True)
    dzen_link = models.URLField(verbose_name='Дзен', blank=True, null=True)
    telegram_link = models.URLField(verbose_name='Telegram', blank=True, null=True)
    whatsapp_link = models.URLField(verbose_name='WhatsApp', blank=True, null=True)

    def __repr__(self):
        return f'{self.__class__}'

    def __str__(self):
        return 'Настройки'

    def is_contacts(self):
        return True if self.contact_description is not None or self.phone is not None or self.email is not None or self.address is not None else False


class CustomPerson(AbstractUser):
    """ Extension for basic user model """
    userpic = models.ImageField(upload_to='img/userpic/', verbose_name='Изображение', help_text='Изображение пользователя', blank=True, null=True)
    middle_name = models.CharField(max_length=50, verbose_name='Отчество', blank=True)
    mobile = models.CharField(validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')], max_length=17, help_text='Введите номер телефона в формате: +999999999', verbose_name='Телефон', blank=True)
    birthday = models.DateField(max_length=10, blank=True, null=True, verbose_name='Дата рождения')
    note = models.TextField(max_length=200, verbose_name='Примечание', blank=True)
    alternative_email = models.EmailField(blank=True, verbose_name='Альтернативный адрес электронной почты')

    def __repr__(self):
        return f'{self.__class__}: {self.pk} {self.username}'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    @property
    @admin.display(description="ФИО")
    def get_fullname(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'


class Department(models.Model):

    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'
        ordering = ('short_name',)

    name = models.CharField(max_length=200, verbose_name='Наименование', help_text='Полное наименование')
    short_name = models.CharField(max_length=50, verbose_name='Сокращение', help_text='Сокращенное название')
    phone = models.CharField(validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')], max_length=17, verbose_name='Телефон', help_text='Введите номер телефона в формате: +999999999', blank=True)
    coordinate = models.CharField(max_length=500, verbose_name='Адрес', help_text='Введите адрес расположения площадки', blank=True)
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Руководитель', null=True, blank=True, related_name='department_supervisor_to_customperson_id_fkey')

    def __repr__(self):
        return f'{self.__class__}: {self.pk} {self.name}'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        # TODO: Переделать в short_name
        return reverse('schedule_home', args=[str(self.pk)])


class Auditory(models.Model):

    class Meta:
        verbose_name = 'Аудитория'
        verbose_name_plural = 'Аудитории'
        ordering = ('number',)

    number = models.CharField(max_length=10, help_text='Номер аудитории', verbose_name='Номер')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, default=None, verbose_name='Площадка', related_name='auditory_department_to_department_id_fkey')

    def __repr__(self):
        return f'{self.__class__}: {self.pk} {self.department} {self.number}'

    def __str__(self):
        return f'{self.department} {self.number}'