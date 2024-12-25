from django.views import View
from django.shortcuts import render

from college.models import Department
from ..models import Couple


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
