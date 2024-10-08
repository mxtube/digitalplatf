from django.contrib import admin
from .models import Profession, Discipline, Studygroup
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):

    list_display = ('number', 'name', 'shortname',)
    list_display_links = ('number', 'name')
    search_fields = ('number', 'name')
    list_filter = (('department', RelatedDropdownFilter),)

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


@admin.register(Studygroup)
class StudyGroupAdmin(admin.ModelAdmin):

    list_display = ('name', 'admin_name', 'profession', 'supervisor', 'assistant',)
    list_display_links = ('name', 'admin_name',)
    list_filter = (('department', RelatedDropdownFilter), ('profession', RelatedDropdownFilter),)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Информация о группе', {
            'fields': (('name', 'admin_name', 'slug'), 'start_edu', 'profession', 'department'),
        }),
        ('Права доступа', {
            'fields': ('supervisor', 'assistant'),
        }),
    )
