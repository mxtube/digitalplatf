from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views import View
from django.shortcuts import render

from college.models import CustomPerson, Department
from ..models import Type, Reference, ReferenceNotify
from ..forms import (ReferenceChooseForm, ReferenceMilitaryForm, ReferenceGrandForm, ReferenceDiplomaForm,
                     ReferenceEducationForm)


class ReferenceHome(LoginRequiredMixin, View):
    """ Контроллер отображения страницы заказа справок """

    template_name = 'references/index.html'
    choose_form = ReferenceChooseForm
    title = 'Справки'
    subtitle = 'Новое заявление'
    references_example = Type.objects.all()

    @staticmethod
    def _reference_list(choose_form: str = ""):
        """ Метод получения формы по названию """
        if choose_form == 'В военкомат':
            return ReferenceMilitaryForm
        elif choose_form == 'Стипендия':
            return ReferenceGrandForm
        elif choose_form == 'Обучение':
            return ReferenceDiplomaForm
        elif choose_form == 'Копия аттестата':
            return ReferenceEducationForm

    def _save_reference(self, data, request):
        """ Метод сохранения нового заказа справки """
        user = CustomPerson.get_user_by_fio(fio=data['student'])
        reference_type = Type.objects.get(name=data['type'])
        new_reference = Reference()
        new_reference.user = user
        new_reference.type = reference_type
        if 'comment' in data:
            new_reference.comment = data['comment']
        new_reference.reference_count = data['count']
        new_reference.save()
        self._send_notify(new_reference)
        return HttpResponseRedirect('history')

    def _send_notify(self, reference):
        """ Метод оповещения о новой заявки на почту """
        subject = 'Цифровая платформа КП11 - Новая заявка на получение справки'
        from_email = 'k31101993@yandex.ru'
        department = Department.objects.get(name=reference.user.group.department)
        to = ReferenceNotify.get_emails_by_department(department=department)
        context = {
            'title': 'Зарегистрирована новая заявка на получение справки',
            'reference': reference
        }
        html_content = render_to_string('emails/new_reference_email.html', context=context)
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def get(self, request):
        """ Метод обработки GET запроса получения страницы с заказом справок """
        context = {
            'title': self.title,
            'reference_example': self.references_example,
            'choose_form': self.choose_form,
            'subtitle': self.subtitle
        }
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        """ Метод обработки POST запроса на странице с заказом справок """
        choose_form = ReferenceChooseForm(request.POST)
        if choose_form.is_valid():
            selected_type = str(choose_form.cleaned_data['type'])
            get_choose_form = self._reference_list(selected_type)
            form = get_choose_form(initial={
                'type': selected_type,
                'student': self.request.user
            })
            context = {
                'title': self.title,
                'subtitle': self.subtitle,
                'reference_example': self.references_example,
                'choose_form': self.choose_form,
                'get_choose_form': form
            }
            return render(request, template_name=self.template_name, context=context)
        elif request.method == 'POST' and 'btn_reference_order' in request.POST:
            form = self._reference_list(request.POST.get('type'))
            clean_form = form(request.POST)
            if clean_form.is_valid():
                return self._save_reference(clean_form.cleaned_data, request)
            context = {
                'title': self.title,
                'subtitle': self.subtitle,
                'reference_example': self.references_example,
                'choose_form': self.choose_form
            }
            return render(request, template_name=self.template_name, context=context)
