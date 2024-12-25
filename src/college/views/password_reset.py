from django.views import View
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from django.shortcuts import render, redirect

from core.settings.components.emails import EMAIL_HOST_USER
from core.ldap import search_and_modify_password
from ..forms import CustomPasswordResetForm


class CustomPasswordResetView(View):
    # https://docs.djangoproject.com/en/5.1/topics/auth/default/#django.contrib.auth.views.PasswordResetView
    form_class = CustomPasswordResetForm
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')

    def get(self, request):
        form = self.form_class()
        context = {
            'title': 'Восстановление пароля',
            'form': form
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            new_password = get_random_string(length=12)

            if search_and_modify_password(user.username, new_password):

                context = {
                    'title': 'Данные об учетной записи',
                    'password': new_password,
                    'user': user.username
                }
                html_content = render_to_string('registration/password_reset_email.html', context=context)
                text_content = strip_tags(html_content)

                send_mail(
                    subject="Цифровая платформа КП11 - Восстановление пароля",
                    message=text_content,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
                return redirect('password_reset_done')
        return render(request, self.template_name, context={'title': 'Восстановление пароля', 'form': form})
