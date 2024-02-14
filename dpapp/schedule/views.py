from django.shortcuts import render
from django.views import View


class ScheduleHome(View):

    template_name = 'schedule/index.html'

    def get(self, request, pk):
        return render(request, template_name=self.template_name)