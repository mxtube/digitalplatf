import datetime
from django.views import View
from django.shortcuts import render

from college.models import CustomPerson
from ..models import Schedule


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
