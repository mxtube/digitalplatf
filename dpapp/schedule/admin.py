from django.contrib import admin
from .models import Stream, GroupStream, Couple


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):

    list_display = ('number',)


@admin.register(GroupStream)
class GroupStreamAdmin(admin.ModelAdmin):

    list_display = ('stream', 'group',)
    list_filter = ('group__department', )


@admin.register(Couple)
class CoupleAdmin(admin.ModelAdmin):

    list_display = ('stream', 'number', 'time_start', 'time_end', 'department',)
    list_filter = ('stream', 'department')