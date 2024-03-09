import datetime, locale
from django.shortcuts import render, get_object_or_404
from django.views import View
from college.models import Department
from educationpart.models import Studygroup
from .models import ChangeSchedule, BaseSchedule, Couple, DayWeek
from schedule.forms import UploadBaseScheduleForm, UploadChangeScheduleForm, ScheduleDateForm, ScheduleTeacherForm

# Настройки для отображения даты и времени на Русском
# TODO: Убрать сделать глобально
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class ScheduleHome(View):

    template_name = 'schedule/index.html'
    date_form = ScheduleDateForm
    teacher_form = ScheduleTeacherForm

    def __number_week(self, date: datetime.date) -> str:
        return 'Четная' if date.isocalendar()[1] % 2 == 0 else 'Нечетная'

    def get_base_or_change_schedule(self, date: datetime.date, department):
        # TODO: Добавить обработку для изменений
        if ChangeSchedule.objects.filter(date=date).exists():
            return ChangeSchedule.objects.filter(date=date)
        else:
            day = date.strftime("%A").capitalize()
            from_day = DayWeek.objects.get(name=day, week__name=self.__number_week(date))
            schedule = BaseSchedule.objects.all().filter(dayweek=from_day, group__department=department)
            return Studygroup.objects.all().filter(department=department.id, id__in=schedule.values('group'))

    def get(self, request, department_name):

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