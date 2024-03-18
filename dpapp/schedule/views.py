import datetime
import locale
import os
from core import settings
from django.shortcuts import render, get_object_or_404
from django.views import View
from schedule.forms import UploadSchedulesFormAdmin, ScheduleDateForm, ScheduleTeacherForm, DepartmentForm
from .models import Schedule, Couple
from college.models import Department
from educationpart.models import Studygroup
from schedule_parsing.parsing import Parsing

# Настройки для отображения даты и времени на Русском
# TODO: Убрать сделать глобально
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class ScheduleHome(View):
    """ Контроллер отображения расписания на главной странице """

    template_name = 'schedule/index.html'
    date_form = ScheduleDateForm
    teacher_form = ScheduleTeacherForm

    def get(self, request, department_name):
        """ Метод обработки GET запроса получения страницы с расписанием """
        department = get_object_or_404(Department, slug=department_name)
        to_day = datetime.date.today()
        groups = Schedule.objects.filter(
            date=to_day, group__department=department
        ).order_by('group__name').distinct('group__name')
        context = {
            'title': department.short_name,
            'subtitle': f'Расписание на {to_day.strftime("%A %d %B %Y")}',
            'department': department,
            'groups': groups,
            'date': to_day.strftime('%Y-%m-%d'),
            'date_form': self.date_form,
            'teacher_form': self.teacher_form
        }
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        """ Метод обработки POST запроса получения страницы с расписанием """
        department = get_object_or_404(Department, slug=kwargs.get('department_name'))
        form = self.date_form(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data.get('date')
            groups = Schedule.objects.filter(
                date=selected_date, group__department=department
            ).order_by('group__name').distinct('group__name')
            context = {
                'title': department.short_name,
                'subtitle': f'Расписание на {selected_date.strftime("%A %d %B %Y")}',
                'department': department,
                'groups': groups,
                'date_form': self.date_form(initial={'date': selected_date}),
                'teacher_form': self.teacher_form
            }
            return render(request, template_name=self.template_name, context=context)


class ScheduleDetailGroup(View):

    template_name = 'schedule/detail.html'

    def get(self, request, department_name, group, date):
        group = get_object_or_404(Studygroup, department__slug=department_name, slug=group)
        department = get_object_or_404(Department, slug=department_name)
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        context = {
            'title': '%s %s' % (department.short_name, group.name),
            'subtitle': 'Расписание на %s' % (date.strftime("%A %d %B")),
            'schedule': Schedule.objects.filter(date=date, group=group).order_by('couple')
        }
        return render(request, template_name=self.template_name, context=context)


class ScheduleRing(View):
    """
    Класс отображения расписания звонков
    """

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


class UploadSchedule(View):
    """ Класс загрузки изменений в расписание в административной панели """
    template_name = 'admin/schedule/upload_schedule.html'
    upload_form = UploadSchedulesFormAdmin
    context = {'title': 'Загрузить изменение в расписание', 'form': upload_form}
    PATH = settings.MEDIA_ROOT + 'xls/schedparsing/'

    def handle_uploaded_file(self, f):
        with open(self.PATH + f.name, "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return True if os.path.exists(self.PATH + f.name) else False

    def get(self, request):
        return render(request, template_name=self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        self.upload_form = self.upload_form(request.POST, request.FILES)
        if self.upload_form.is_valid():
            file = self.upload_form.cleaned_data['file']
            start_row = self.upload_form.cleaned_data['start_row']
            date_start = self.upload_form.cleaned_data['start_date'].strftime('%Y-%m-%d')
            date_end = self.upload_form.cleaned_data['end_date'].strftime('%Y-%m-%d')
            day = self.upload_form.cleaned_data.get('day').__str__()
            if self.handle_uploaded_file(file):
                department = self.upload_form.cleaned_data['department']
                parse = Parsing(filename=file, start_row=start_row)
                parse.start(department, date_start, date_end, day)
        self.context['form'] = self.upload_form
        return render(request, template_name=self.template_name, context=self.context)


class ScheduleDashboard(View):
    """
    Класс отображения аналитики расписания в административной панели
    """
    template_name = 'admin/schedule/dashboard.html'
    department_form = DepartmentForm
    context = {}

    def get(self, request):
        self.context['change_schedule'] = Schedule.objects.all()
        self.context['department_form'] = self.department_form
        return render(request, template_name=self.template_name, context=self.context)