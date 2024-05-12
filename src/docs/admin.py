from django.contrib import admin
from django.contrib import messages
from .forms import ArticleAdminForm
from .models import Category, Article
from django.utils.translation import ngettext


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug',)
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    form = ArticleAdminForm
    list_display = ('name', 'slug', 'is_active',)
    list_filter = ('category', 'is_active',)
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    actions = ['unpublish_article', 'publish_article']

    @admin.action(description='Снять с публикации')
    def unpublish_article(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            ngettext(
                "%d статья была успешно снята с публикации.",
                "%d статьи были успешно сняты с публикации.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.action(description='Опубликовать')
    def publish_article(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            ngettext(
                "%d статья была успешно опубликована.",
                "%d статьи были успешно опубликованы.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )
