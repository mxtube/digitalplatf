import pytest
from django.urls import reverse
from django.test import Client
from datetime import date


# @pytest.mark.django_db
# def test_schedule_home_get(department, schedule):
#     """Test the GET method of the ScheduleHome view."""
#     client = Client()
#     url = reverse('schedule_home', args=[department.slug])
#
#     response = client.get(url)
#
#     assert response.status_code == 200
#     assert 'title' in response.context
#     assert response.context['title'] == department.short_name
#     assert 'groups' in response.context
#     assert response.context['groups'].first().group.name == schedule.group.name
#     assert response.template_name[0] == 'schedule/index.html'
#
#
# @pytest.mark.django_db
# def test_schedule_home_post_valid_date(department, schedule):
#     """Test the POST method of the ScheduleHome view with a valid date."""
#     client = Client()
#     url = reverse('schedule_home', args=[department.slug])
#     valid_date = date.today()
#
#     # Simulate form submission with a valid date
#     response = client.post(url, {'date': valid_date})
#
#     assert response.status_code == 200
#     assert 'subtitle' in response.context
#     assert valid_date.strftime('%d %B') in response.context['subtitle']
#     assert response.template_name[0] == 'schedule/index.html'
#
#
# @pytest.mark.django_db
# def test_schedule_home_post_invalid_date(department):
#     """Test the POST method of the ScheduleHome view with an invalid date."""
#     client = Client()
#     url = reverse('schedule_home', args=[department.slug])
#
#     # Simulate form submission with an invalid date (e.g., future date or invalid format)
#     invalid_date = '2025-01-01'  # Use an invalid or future date
#     response = client.post(url, {'date': invalid_date})
#
#     assert response.status_code == 200
#     assert 'date_form' in response.context  # Ensure the form is included in the context
#     assert 'teacher_form' in response.context  # Ensure the teacher form is also in the context
#     assert response.template_name[0] == 'schedule/index.html'
#
#
# @pytest.mark.django_db
# def test_schedule_home_post_teacher_redirect(department, schedule):
#     """Test the POST method of the ScheduleHome view with a teacher form."""
#     client = Client()
#     url = reverse('schedule_home', args=[department.slug])
#
#     # Simulate form submission with a teacher selected
#     teacher = schedule.teacher  # Assuming a schedule object has a teacher field
#     response = client.post(url, {'teacher': teacher.id})
#
#     assert response.status_code == 302  # Redirect
#     assert response.url == teacher.get_absolute_url_teacher()  # Assuming get_absolute_url_teacher() method exists
