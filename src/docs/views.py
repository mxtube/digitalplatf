from django.shortcuts import render
from .models import Article, Category
from django.views.generic import ListView, DetailView, View


class DocsHomePage(ListView):

    template_name = 'docs/index.html'
    model = Article
    context_object_name = 'article'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'КП Справка'
        context['subtitle'] = 'Документация по сервисам'
        return context

    def get_queryset(self):
        return Article.objects.filter(is_active=True).order_by('category')


class CategoryPage(ListView):
    pass


class ArticlePage(DetailView):
    pass


