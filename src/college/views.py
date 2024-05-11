from django.views import View
from .forms import SuggestionForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
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

    def get(self, request):
        user_services = UserServices.objects.filter(visible=True)
        context = {
            'title': 'Профиль пользователя',
            'subtitle': request.user.username,
            'user_services': user_services
        }
        return render(request=request, template_name=self.template_name, context=context)

class SuggestionPage(LoginRequiredMixin, View):

    template_name = 'college/suggestion.html'
    form = SuggestionForm

    def get(self, request):
        self.form = SuggestionForm(initial={'user': request.user.username })
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
