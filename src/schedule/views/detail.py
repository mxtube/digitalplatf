from django.views import View
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from college.models import Department
from ..models import Schedule


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
