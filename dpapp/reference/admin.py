from django.contrib import admin
from .models import Status


@admin.register(Status)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
