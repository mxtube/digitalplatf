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

    def __number_week(self, date: datetime.date) -> str:
        """ Методы получения четности недели """
        return 'Четная' if date.isocalendar()[1] % 2 == 0 else 'Нечетная'

    def get_base_or_change_schedule(self, date: datetime.date, department):
        """
        Метод получения расписания/расписания с изменениями в зависимости от даты
        """
        if ChangeSchedule.objects.filter(date=date).exists():
            schedule = ChangeSchedule.objects.all().filter(date=date, group__department=department)
            groups = Studygroup.objects.all().filter(department=department.id, id__in=schedule.values(
                'group')).order_by('profession')
            return groups
        else:
            day = date.strftime("%A").capitalize()
            from_day = DayWeek.objects.get(name=day, week__name=self.__number_week(date))
            schedule = BaseSchedule.objects.all().filter(dayweek=from_day, group__department=department)
            groups = Studygroup.objects.all().filter(department=department.id, id__in=schedule.values(
                'group')).order_by('profession')
            return groups

    def get(self, request, department_name):
        """
        Метод отображения страницы при GET запросе
        """
        department = get_object_or_404(Department, slug=department_name)
        to_day = datetime.date.today()
        context = {
            'title': department.short_name,
            'subtitle': f'Расписание на {to_day.strftime("%A %d %B %Y")}',
            'department': department,
            'groups': self.get_base_or_change_schedule(to_day, department),
            'date': to_day.strftime('%Y-%m-%d'),
            'date_form': self.date_form,
            'teacher_form': self.teacher_form
        }
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        """
        Метод отображения страницы при POST запросе
        """
        form = self.date_form(request.POST)
        department = get_object_or_404(Department, slug=kwargs.get('department_name'))
        if form.is_valid():
            selected_date = form.cleaned_data.get('date')
            context = {
                'title': department.short_name,
                'subtitle': f'Расписание на {selected_date.strftime("%A %d %B %Y")}',
                'department': department,
                'groups': self.get_base_or_change_schedule(selected_date, department),
                'date_form': self.date_form(initial={'date': selected_date}),
                'teacher_form': self.teacher_form
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