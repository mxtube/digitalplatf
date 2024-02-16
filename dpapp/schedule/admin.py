from django.contrib import admin
from .models import Stream, GroupStream, Couple, ScheduleCalendarMark, ScheduleCalendar


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


@admin.register(ScheduleCalendarMark)
class ScheduleCalendarMarkAdmin(admin.ModelAdmin):

    list_display = ('name', 'symbol',)


@admin.register(ScheduleCalendar)
class ScheduleCalendarAdmin(admin.ModelAdmin):

    list_display = ('start_week', 'end_week', 'group', 'mark')
    list_filter = ('group__department', 'group__name', 'start_week',)
