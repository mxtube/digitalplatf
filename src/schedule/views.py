import os
import locale
import datetime
from core import settings
from django.views import View
from .tasks import upload_schedule
from .models import Schedule, Couple
from django.shortcuts import redirect
from educationpart.models import Studygroup
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from schedule_parsing.parsing import Parsing
from college.models import Department, CustomPerson
from django.shortcuts import render, get_object_or_404
from schedule.forms import UploadSchedulesFormAdmin, ScheduleDateForm, ScheduleTeacherForm, DashboardForm

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
        schedule = Schedule.objects.filter(date=to_day, group__department=department)
        context = {
            'title': department.short_name,
            'subtitle': f'Расписание на {to_day.strftime("%d %B")}',
            'department': department,
            'groups': schedule.order_by('group__name').distinct('group__name'),
            'date': to_day.strftime('%Y-%m-%d'),
            'date_form': self.date_form
        }
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        """ Метод обработки POST запроса получения страницы с расписанием """
        department = get_object_or_404(Department, slug=kwargs.get('department_name'))
        date_form = self.date_form(request.POST)
        teacher_form = self.teacher_form(request.POST)

        if date_form.is_valid():
            selected_date = date_form.cleaned_data.get('date')
            schedule = (Schedule.objects.filter(date=selected_date).filter(group__department=department)
                        .select_related('group', 'group__department', 'group__profession', 'couple', 'teacher',
                                        'discipline', 'auditory'))
            context = {
                'title': department.short_name,
                'subtitle': f'Расписание на {selected_date.strftime("%d %B")}',
                'department': department,
                'groups': schedule.order_by('group__name').distinct('group__name'),
                'date': selected_date.strftime('%Y-%m-%d'),
                'date_form': self.date_form(initial={'date': selected_date}),
                'teacher_form': self.teacher_form(queryset=schedule.order_by('teacher').distinct('teacher'))
            }
            return render(request, template_name=self.template_name, context=context)
        elif teacher_form.is_valid():
            selected_item = teacher_form.cleaned_data['teacher']
            return redirect(selected_item.get_absolute_url_teacher())
        else:
            return HttpResponseRedirect(f'/schedule/{department.slug}')


class ScheduleDetail(View):

    template_name = 'schedule/detail_all.html'

    def get(self, request, department_name, date):
        department = get_object_or_404(Department, slug=department_name)
        schedule = (Schedule.objects.filter(date=date, group__department__slug__contains=department.slug)
                    .select_related('group', 'couple', 'teacher', 'discipline', 'auditory'))
        page_num = request.GET.get('page', 1)
        paginator = Paginator(schedule.values_list('group', flat=True).distinct(), 4)
        page_obj = paginator.page(page_num)
        context = {
            'title': f'Расписание {department.short_name}',
            'subtitle': f'на {date}',
            'schedule': schedule.filter(group__in=page_obj.object_list),
            'pagination_pages': page_obj
        }
        return render(request, template_name=self.template_name, context=context)


class ScheduleDetailGroup(View):
    template_name = 'schedule/detail.html'

    def get(self, request, department_name, group, date):
        group = get_object_or_404(Studygroup, department__slug=department_name, slug=group)
        department = get_object_or_404(Department, slug=department_name)
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        schedule = Schedule.objects.filter(date=date, group=group).order_by('couple').select_related(
            'group', 'couple', 'teacher', 'discipline', 'auditory')
        context = {
            'title': '%s %s' % (department.short_name, group.name),
            'subtitle': 'Расписание на %s' % (date.strftime("%A %d %B")),
            'schedule': schedule
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
    """ Класс отображения расписания звонков """

    template_name = 'schedule/rings.html'

    def get(self, request, department_name):
        couple = Couple.objects.filter(department__slug=department_name).select_related('department', 'stream')
        department = Department.objects.get(slug=department_name)
        context = {
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

    def handle_uploaded_file(self, file, department: Department):
        path = self.PATH + department.slug + '/'
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        with open(path + file.name, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return True if os.path.exists(path + file.name) else False

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
            department = self.upload_form.cleaned_data['department']
            if self.handle_uploaded_file(file, department):
                upload_schedule.delay(
                    file=str(file),
                    start_row=start_row,
                    department=department.name,
                    date_start=date_start,
                    date_end=date_end,
                    day=day
                )
        self.context['form'] = self.upload_form
        return render(request, template_name=self.template_name, context=self.context)


class ScheduleDashboard(View):
    """ Класс отображения аналитики расписания в административной панели """
    template_name = 'admin/schedule/dashboard.html'
    dashboard_form = DashboardForm
    context = {'title': 'Dashboard', 'subtitle': 'Статистика по площадкам'}

    def get(self, request):
        context = {'dashboard_form': self.dashboard_form}
        return render(request, template_name=self.template_name, context=self.context | context)

    def post(self, request, *args, **kwargs):
        dashboard_form = self.dashboard_form(request.POST)
        if dashboard_form.is_valid():
            selected_data = dashboard_form.cleaned_data
            date = selected_data['date']
            department = selected_data['department']
        context = {'dashboard_form': dashboard_form}
        return render(request, template_name=self.template_name, context=self.context | context)
