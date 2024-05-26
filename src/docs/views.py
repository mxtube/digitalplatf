from .models import Article, Category
from django.views.generic import ListView, DetailView


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

    model = Article
    template_name = 'docs/category.html'
    context_object_name = 'articles'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'КП Справка'
        context['subtitle'] = Category.objects.get(slug=self.kwargs['category_name']).name
        return context

    def get_queryset(self):
        return Article.objects.filter(is_active=True, category__slug=self.kwargs['category_name']).order_by('name')


class ArticlePage(DetailView):

    model = Article
    template_name = 'docs/article.html'
    context_object_name = 'article'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'КП Справка'
        context['subtitle'] = Category.objects.get(slug=self.kwargs['category_name']).name
        return context

    def get_object(self, *, object_list=None, **kwargs):
        return Article.objects.get(
            is_active=True,
            slug=self.kwargs['article_name'],
            category__slug=self.kwargs['category_name']
        )
