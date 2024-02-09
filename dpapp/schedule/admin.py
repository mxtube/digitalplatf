from django.contrib import admin
from .models import Stream


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):

    list_display = ('number',)
