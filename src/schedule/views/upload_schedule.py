import os
from django.views import View
from django.shortcuts import render

from ..tasks import upload_schedule
from schedule_parsing.parsing import Parsing # noqa F401
from college.models import Department
from schedule.forms import UploadSchedulesFormAdmin


class UploadSchedule(View):
    """ Класс загрузки изменений в расписание в административной панели """
    template_name = 'admin/schedule/upload_schedule.html'
    upload_form = UploadSchedulesFormAdmin
    context = {'title': 'Загрузить изменение в расписание', 'form': upload_form}
    PATH = 'xls/schedparsing/'

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
            print(type(date_start), type(date_end), type(day))
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
                self.context['message'] = 'Файл с расписанием загружен'
        self.context['form'] = self.upload_form
        return render(request, template_name=self.template_name, context=self.context)
