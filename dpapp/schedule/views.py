import os
import locale
import datetime
from core import settings
from django.views import View
from .models import Schedule, Couple
from educationpart.models import Studygroup
from django.http import HttpResponseRedirect
from schedule_parsing.parsing import Parsing
from college.models import Department, CustomPerson
from django.shortcuts import render, get_object_or_404
from schedule.forms import UploadSchedulesFormAdmin, ScheduleDateForm, ScheduleTeacherForm, DepartmentForm

# Настройки для отображения даты и времени на Русском
# TODO: Убрать сделать глобально
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class ScheduleHome(View):
    """ Контроллер отображения расписания на главной странице """

    template_name = 'schedule/index.html'
    date_form = ScheduleDateForm
    teacher_form = ScheduleTeacherForm
    context = {}

    def get(self, request, department_name):
        """ Метод обработки GET запроса получения страницы с расписанием """
        department = get_object_or_404(Department, slug=department_name)
        to_day = datetime.date.today()
        schedule = Schedule.objects.filter(date=to_day, group__department=department)
        self.context['title'] = department.short_name
        self.context['subtitle'] = f'Расписание на {to_day.strftime('%d %B')}'
        self.context['department'] = department
        self.context['groups'] = schedule.order_by('group__name').distinct('group__name')
        self.context['date_form'] = self.date_form
        return render(request, template_name=self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        """ Метод обработки POST запроса получения страницы с расписанием """
        department = get_object_or_404(Department, slug=kwargs.get('department_name'))
        date_form = self.date_form(request.POST)
        user_form = self.teacher_form(request.POST)
        self.context['title'] = department.short_name

        if date_form.is_valid():
            selected_date = date_form.cleaned_data.get('date')
            schedule = Schedule.objects.filter(date=selected_date, group__department=department)
            self.context['subtitle'] = f'Расписание на {selected_date.strftime('%d %B')}'
            self.context['department'] = department
            self.context['groups'] = schedule.order_by('group__name').distinct('group__name')
            self.context['date_form'] = self.date_form(initial={'date': selected_date})
            return render(request, template_name=self.template_name, context=self.context)
        if user_form.is_valid():
            selected_item = user_form.cleaned_data['teacher']
            return HttpResponseRedirect(selected_item.get_absolute_url_teacher())
        else:
            return HttpResponseRedirect(f'schedule/{department.slug}')


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


class ScheduleDetailTeacher(View):

    template = 'schedule/detail.html'

    def get(self, request, department_name, teacher, date):
        user = CustomPerson.objects.get(pk=teacher)
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        schedule = Schedule.objects.filter(date=date, teacher=user)
        context = {
            'title': 'Расписание %s' % (user.get_name_initials()),
            'subtitle': 'на %s' % (date.strftime("%d %B")),
            'schedule': schedule
        }
        return render(request, template_name=self.template, context=context)


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