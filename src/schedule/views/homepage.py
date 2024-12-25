import datetime
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect

from schedule_parsing.parsing import Parsing # noqa F401
from college.models import Department
from schedule.forms import ScheduleDateForm, ScheduleTeacherForm
from ..models import Schedule


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
