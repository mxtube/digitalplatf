from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from .models import SiteSettings, CustomPerson


class HomePage(View):

    template_name = 'index.html'

    def get(self, request):
        site_settings = SiteSettings()
        context = {'title': site_settings.site_name}
        return render(request, self.template_name, context=context)


class ProfilePage(LoginRequiredMixin, View):

    template_name = 'registration/profile.html'
    model = CustomPerson
    context = {'title': 'Профиль пользователя'}

    def get(self, request):
        self.context['subtitle'] = request.user.get_full_name
        return render(request=request, template_name=self.template_name, context=self.context)