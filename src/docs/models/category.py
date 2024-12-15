from django.db import models
from django.urls import reverse


class Category(models.Model):

    name = models.CharField(max_length=100, verbose_name='Наименование')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание', blank=True)
    icon = models.CharField(max_length=100, verbose_name='Иконка', help_text='Fontawesome')
    is_active = models.BooleanField(default=True, verbose_name='Видимость')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('docs_category', kwargs={'category_name': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
