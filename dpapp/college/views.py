from django.shortcuts import render
from django.views import View
from .models import SiteSettings

class HomePage(View):

    template_name = 'index.html'

    def get(self, request):
        site_settings = SiteSettings()
        context = {'title': site_settings.site_name}
        return render(request, self.template_name, context=context)
