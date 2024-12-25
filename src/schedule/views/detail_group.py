import datetime
from django.views import View
from django.shortcuts import render, get_object_or_404

from educationpart.models import Studygroup
from college.models import Department
from ..models import Schedule


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
