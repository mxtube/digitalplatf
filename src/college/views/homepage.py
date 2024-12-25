from django.views import View
from django.shortcuts import render
from ..models import SiteSettings


class HomePage(View):

    template_name = 'index.html'

    def get(self, request):
        site_settings = SiteSettings.objects.first()
        if site_settings:
            context = {'title': site_settings.site_name, 'subtitle': site_settings.short_site_name}
        else:
            context = {'title': 'Цифровая', 'subtitle': 'платформа'}
        return render(request, self.template_name, context=context)
