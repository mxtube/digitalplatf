from django.contrib import admin
from .models import Profession, Discipline


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):

    list_display = ('number', 'name', 'shortname',)
    list_display_links = ('number', 'name')
    search_fields = ('number', 'name')
    list_filter = ('department',)

    fieldsets = (
        ('Информация о специальности', {
            'fields': (('number', 'name', 'shortname',)),
            'description': 'Специальность — это отдельная отрасль науки, техники, мастерства или искусства, в которой работают специалисты.',
        }),
        ('Дополнительная информация', {
            'fields': (('department'),),
            'classes': ('wide',),
        }),
    )


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):

    list_display = ('name', )
    list_display_links = ('name', )
    search_fields = ('name',)
