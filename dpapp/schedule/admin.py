from django.contrib import admin
from .views import UploadSchedule, ScheduleDashboard
from django.urls import path
from .models import (Stream, GroupStream, Couple, ScheduleCalendarMark, ScheduleCalendar, Schedule, UploadSchedules,
                     DashboardSchedule)


@admin.register(UploadSchedules)
class UploadSchedulesAdmin(admin.ModelAdmin):
    # TODO: Разобраться с ссылкой

    model = UploadSchedule

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name)
        return [path('', UploadSchedule.as_view(), name=view_name),]


@admin.register(DashboardSchedule)
class DashboardScheduleAdmin(admin.ModelAdmin):

    model = Schedule

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name)
        return [path('', ScheduleDashboard.as_view(), name=view_name),]


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):

    list_display = ('number',)


@admin.register(GroupStream)
class GroupStreamAdmin(admin.ModelAdmin):

    list_display = ('stream', 'group',)
    list_filter = ('group__department', )
    unique_together = ('stream', 'group')


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


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):

    list_display = ('date', 'couple', 'group', 'auditory', 'discipline', 'teacher',)
