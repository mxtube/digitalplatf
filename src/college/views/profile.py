from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import CustomPerson, UserServices


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
