from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import SuggestionForm


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
