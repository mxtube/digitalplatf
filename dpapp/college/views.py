from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from .models import SiteSettings, CustomPerson, UserServicesCategory, UserServices


class HomePage(View):

    template_name = 'index.html'

    def get(self, request):
        site_settings = SiteSettings().load()
        context = {'title': site_settings.site_name, 'subtitle': site_settings.short_site_name}
        return render(request, self.template_name, context=context)


class ProfilePage(LoginRequiredMixin, View):

    template_name = 'registration/profile.html'
    model = CustomPerson
    context = {'title': 'Профиль пользователя'}

    def get(self, request):
        self.context['subtitle'] = request.user.get_full_name
        user_services = UserServices.objects.filter(visible=True)
        self.context['user_services'] = user_services
        return render(request=request, template_name=self.template_name, context=self.context)
