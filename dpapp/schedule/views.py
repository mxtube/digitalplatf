import datetime
from django.shortcuts import render
from django.views import View
from college.models import Department
from .models import ChangeSchedule, BaseSchedule
from schedule.forms import UploadBaseScheduleForm, UploadChangeScheduleForm


class ScheduleHome(View):

    template_name = 'schedule/index.html'
    context = {'title': 'Расписание'}

    def get(self, request, pk):
        department = Department.objects.get(pk=pk)
        self.context['subtitle'] = department.short_name
        self.context['date'] = datetime.date.today().strftime('%Y-%m-%d')
        return render(request, template_name=self.template_name, context=self.context)


class UploadBaseSchedule(View):

    template_name = 'admin/schedule/upload_schedule.html'

    def get(self, request):
        context = {'title': 'Загрузить расписание на семестр', 'form': UploadBaseScheduleForm()}
        return render(request, template_name=self.template_name, context=context)


class UploadChangeSchedule(View):

    template_name = 'admin/schedule/upload_schedule.html'

    def get(self, request):
        context = {'title': 'Загрузить изменение в расписание', 'form': UploadChangeScheduleForm()}
        return render(request, template_name=self.template_name, context=context)


class ScheduleDashboard(View):

    template_name = 'admin/schedule/dashboard.html'
    context = {}

    def get(self, request):
        self.context['base_schedule'] = BaseSchedule.objects.all()
        self.context['change_schedule'] = ChangeSchedule.objects.all()
        return render(request, template_name=self.template_name)