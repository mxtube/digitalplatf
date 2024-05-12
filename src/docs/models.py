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


class Article(models.Model):

    category = models.ForeignKey(Category, on_delete=models.PROTECT,verbose_name='Категория',
                                 related_name='article_cat_to_cat_id_fkey')
    name = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return f'{self.category} - {self.name}'

    def get_absolute_url(self):
        return reverse('docs_article', kwargs={'category_name': self.category.slug, 'article_name': self.slug})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
