import datetime
from django.shortcuts import render
from django.views import View
from college.models import Department


class ScheduleHome(View):

    template_name = 'schedule/index.html'
    context = {'title': 'Расписание'}

    def get(self, request, pk):
        department = Department.objects.get(pk=pk)
        self.context['subtitle'] = department.short_name
        self.context['date'] = datetime.date.today().strftime('%Y-%m-%d')
        return render(request, template_name=self.template_name, context=self.context)