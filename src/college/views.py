from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from core.settings import EMAIL_HOST_USER
from core.ldap import search_and_modify_password
from .forms import SuggestionForm, EditProfileForm, CustomPasswordResetForm
from .models import SiteSettings, CustomPerson, UserServices


class HomePage(View):

    template_name = 'index.html'

    def get(self, request):
        site_settings = SiteSettings.objects.first()
        if site_settings:
            context = {'title': site_settings.site_name, 'subtitle': site_settings.short_site_name}
        else:
            context = {'title': 'Цифровая', 'subtitle': 'платформа'}
        return render(request, self.template_name, context=context)


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


class ProfilePage(LoginRequiredMixin, View):

    template_name = 'registration/profile.html'
    model = CustomPerson

    def get(self, request):
        user_services = UserServices.objects.filter(visible=True)
        context = {
            'title': 'Профиль пользователя',
            'subtitle': request.user.username,
            'user_services': user_services
        }
        return render(request=request, template_name=self.template_name, context=context)


class ProfileEditPage(LoginRequiredMixin, View):

    template_name = 'registration/profile_edit.html'
    form = EditProfileForm

    def get(self, request):
        person = CustomPerson.objects.get(pk=request.user.pk)
        self.form = EditProfileForm(instance=person)
        context = {
            'title': 'Профиль пользователя',
            'subtitle': 'Редактирование',
            'form': self.form
        }
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        person = CustomPerson.objects.get(pk=request.user.pk)
        form = self.form(request.POST, instance=person)
        context = {
            'title': 'Профиль пользователя',
            'subtitle': 'Редактирование',
            'form': self.form(instance=person)
        }
        if form.is_valid():
            form.save()
            return redirect(to='profile')
        else:
            context['form'] = form
        return render(request, self.template_name, context=context)


class SuggestionPage(LoginRequiredMixin, View):

    template_name = 'college/suggestion.html'
    form = SuggestionForm

    def get(self, request):
        self.form = SuggestionForm(initial={'user': request.user.username})
        context = {
            'title': 'Обратная связь',
            'subtitle': 'Идеи и предложения',
            'form': self.form
        }
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        self.form = SuggestionForm(initial={'user': request.user.username})
        context = {
            'title': 'Обратная связь',
            'subtitle': 'Идеи и предложения',
            'form': self.form,
        }
        return render(request=request, template_name=self.template_name, context=context)
