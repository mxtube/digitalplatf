from django.views import View
from django.shortcuts import render

from schedule.forms import DashboardForm


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
            date = selected_data['date'] # noqa F841
            department = selected_data['department'] # noqa F841
        context = {'dashboard_form': dashboard_form}
        return render(request, template_name=self.template_name, context=self.context | context)
