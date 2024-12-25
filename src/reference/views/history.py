from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render

from ..models import Reference


class ReferenceHistory(LoginRequiredMixin, View):
    """ Контроллер отображения страницы с историей заявок на получение справки """
    template_name = 'references/history.html'

    def get(self, request, *args, **kwargs):
        """ Метод обработки GET запрос получения страницы с историей справок """
        history = Reference.objects.filter(user=request.user.pk).order_by('-created_at')
        context = {
            'title': 'Справки',
            'subtitle': 'История заказов',
            'references': history
        }
        return render(request, template_name=self.template_name, context=context)
