from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class SiteSettings(models.Model):

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'

    site_name = models.TextField(verbose_name='Полное название сайта', max_length=200, default='Цифровая платформа')
    short_site_name = models.CharField(verbose_name='Краткое название сайта', max_length=31)
    logotype = models.ImageField(verbose_name='Логотип', upload_to='img', name='logotype', blank=True, null=True)
    description = models.TextField(verbose_name='Описание главной страницы')

    # Contacts
    contact_description = models.TextField(verbose_name='Об организации', max_length=200, blank=True, null=True)
    phone = PhoneNumberField(verbose_name='Телефон', help_text='Например: +999999999', region='', blank=True, null=True)
    email = models.EmailField(verbose_name='Электронная почта', help_text='Пример: example@mail.ru', blank=True,
                              null=True)
    address = models.CharField(verbose_name='Адрес', help_text='Пример: 129344, г. Москва, Проспект мира д.1',
                               max_length=100, blank=True, null=True)

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
        return True if self.contact_description is not None or self.phone is not None or self.email is not None or self.address is not None else False # noqa E501
