import datetime, locale
from django.shortcuts import render, get_object_or_404
from django.views import View
from college.models import Department
from .models import ChangeSchedule, BaseSchedule, Couple
from schedule.forms import UploadBaseScheduleForm, UploadChangeScheduleForm, ScheduleDateForm, ScheduleTeacherForm

# Настройки для отображения даты и времени на Русском
# TODO: Убрать сделать глобально
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class ScheduleHome(View):

    template_name = 'schedule/index.html'

    def get(self, request, department_name):

        department = get_object_or_404(Department, slug=department_name)
        to_day = datetime.date.today()
        context = {
            'subtitle': f'Расписание на {to_day.strftime("%A %d %b %Y")}',
            'title': department.short_name,
            'department': department,
            'date': to_day.strftime('%Y-%m-%d'),
            'date_form': ScheduleDateForm,
            'teacher_form': ScheduleTeacherForm
        }
        return render(request, template_name=self.template_name, context=context)


class ScheduleRing(View):

    template_name = 'schedule/rings.html'

    def get(self, request, department_name):
        couple = Couple.objects.filter(department__slug=department_name)
        department = Department.objects.get(slug=department_name)
        context={
            'title': department.short_name,
            'subtitle': 'Расписание звонков',
            'couples': couple
        }
        return render(request, template_name=self.template_name, context=context)


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