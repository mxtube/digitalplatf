"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import ScheduleHome, ScheduleRing, ScheduleDetailGroup, ScheduleDetailTeacher, ScheduleDetail

urlpatterns = [
    path('<slug:department_name>/', ScheduleHome.as_view(), name='schedule_home'),
    path('<slug:department_name>/rings/', ScheduleRing.as_view(), name='schedule_rings'),
    path('<slug:department_name>/a/<str:date>', ScheduleDetail.as_view(), name='schedule_department'),
    path('<slug:department_name>/g/<str:group>/<str:date>', ScheduleDetailGroup.as_view(), name='schedule_group'),
    path('<slug:department_name>/t/<int:teacher>/<str:date>', ScheduleDetailTeacher.as_view(), name='schedule_teacher'),
]
