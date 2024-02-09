from django.contrib import admin
from .models import Status, Type


@admin.register(Status)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)