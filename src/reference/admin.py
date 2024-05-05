from django.contrib import admin
from .models import Status, Type, Reference

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):

    model = Reference
    list_display = ('get_user', 'get_type', 'comment', 'reference_count', 'status', 'created_at', 'updated_at',)
    list_filter = ('status', 'type',)

    fieldsets = (
        ('Инфомарция о заявителе', {"fields": (('user',)),}),
        ('Инфомарция о справке', {"fields": (('type', 'comment', 'status', 'reference_count',)),}),
    )

    @admin.display(description='Заявитель')
    def get_user(self, obj):
        return f'{obj.user.last_name} {obj.user.first_name} {obj.user.middle_name}'

    @admin.display(description='Тип справки')
    def get_type(self, obj):
        return obj.type.name

    @admin.display(description='Группа')
    def get_studygroup(self, obj):
        return f'{obj.user.studygroup_id}' if obj.user.studygroup_id else 'Отсутствует'

    def get_status(self, obj):
        return obj.status.name


@admin.register(Status)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)