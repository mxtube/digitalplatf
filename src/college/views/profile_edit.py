from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from ..forms import EditProfileForm
from ..models import CustomPerson


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
