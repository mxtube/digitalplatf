import datetime
import locale
import os
from django.shortcuts import render, get_object_or_404
from django.views import View
from college.models import Department
from core import settings
from educationpart.models import Studygroup
from schedule.forms import (UploadBaseScheduleFormAdmin, UploadChangeScheduleFormAdmin, ScheduleDateForm,
                            ScheduleTeacherForm, DepartmentForm)
from schedule_parsing.parsing import Parsing
from .models import ChangeSchedule, BaseSchedule, Couple, DayWeek

# Настройки для отображения даты и времени на Русском
# TODO: Убрать сделать глобально
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class ScheduleHome(View):
    """
    Класс отображения расписания на главной странице
    """

    template_name = 'schedule/index.html'
    date_form = ScheduleDateForm
    teacher_form = ScheduleTeacherForm
    context = {}

    def get(self, request, department_name):
        """
        Метод отображения страницы при GET запросе
        """
        department = get_object_or_404(Department, slug=department_name)
        to_day = datetime.date.today()

        self.context['title'] = department.short_name
        self.context['subtitle'] = f'Расписание на {to_day.strftime("%A %d %B %Y")}'
        self.context['department'] = department
        self.context['date'] = to_day.strftime('%Y-%m-%d')
        self.context['date_form'] = self.date_form
        self.context['teacher_form'] = self.teacher_form
        if ChangeSchedule.has_schedule_by_date(to_day):
            self.context['groups'] = ChangeSchedule.objects.filter(date=to_day, group__department=department).order_by('group__name').distinct('group__name')
        else:
            self.context['groups'] = BaseSchedule().get_schedule_by_date(to_day)
        return render(request, template_name=self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        """
        Метод отображения страницы при POST запросе
        """
        form = self.date_form(request.POST)
        department = get_object_or_404(Department, slug=kwargs.get('department_name'))
        if form.is_valid():
            selected_date = form.cleaned_data.get('date')
            self.context['title'] = department.short_name
            self.context['subtitle'] = f'Расписание на {selected_date.strftime("%A %d %B %Y")}'
            self.context['department'] = department
            self.context['date_form'] = self.date_form(initial={'date': selected_date})
            self.context['teacher_form'] = self.teacher_form
            if ChangeSchedule.has_schedule_by_date(selected_date):
                self.context['groups'] = ChangeSchedule.objects.filter(
                    date=selected_date, group__department=department
                ).order_by('group__name').distinct('group__name')
            else:
                print(BaseSchedule().get_schedule_by_date(selected_date))
                self.context['groups'] = BaseSchedule().get_schedule_by_date(selected_date)
            return render(request, template_name=self.template_name, context=self.context)


class ScheduleDetailGroup(View):

    template_name = 'schedule/detail.html'
    context = {}
    model = None

    def get(self, request, department_name, group, date):
        group = get_object_or_404(Studygroup, department__slug=department_name, slug=group)
        department = get_object_or_404(Department, slug=department_name)
        self.context['title'] = '%s %s' % (department.short_name, group.name)
        if ChangeSchedule.has_schedule_by_date(date):
            self.context['schedule'] = ChangeSchedule.objects.filter(date=date)
        elif BaseSchedule().has_schedule_by_date(date):
            print(BaseSchedule().get_schedule_by_date(date))
            self.context['schedule'] = BaseSchedule().get_schedule_by_date(date)
        return render(request, template_name=self.template_name, context=self.context)


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


class UploadBaseSchedule(View):
    """
    Класс загрузки основного расписания в административной панели
    """
    template_name = 'admin/schedule/upload_schedule.html'
    upload_form = UploadBaseScheduleFormAdmin

    def handle_uploaded_file(self, f):
        with open(f"../dpdata/xls/schedparsing/{f.name}", "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def get(self, request):
        context = {'title': 'Загрузить расписание на семестр', 'upload_form': self.upload_form}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.upload_form(request.POST, request.FILES)
        if form.is_valid():
            self.handle_uploaded_file(form.cleaned_data['file'])
            context = {'title': 'Загрузить расписание на семестр', 'upload_form': self.upload_form}
        return render(request, template_name=self.template_name, context=context)


class UploadChangeSchedule(View):
    """
    Класс загрузки изменений в расписание в административной панели
    """
    template_name = 'admin/schedule/upload_schedule.html'
    upload_form = UploadChangeScheduleFormAdmin
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
            if self.handle_uploaded_file(file):
                department = self.upload_form.cleaned_data['department']
                date = self.upload_form.cleaned_data['date']
                parse = Parsing(filename=file)
                parse.start(department, date)
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
        self.context['base_schedule'] = BaseSchedule.objects.all()
        self.context['change_schedule'] = ChangeSchedule.objects.all()
        self.context['department_form'] = self.department_form
        return render(request, template_name=self.template_name, context=self.context)