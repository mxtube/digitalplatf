import pytest
from django.urls import reverse


class TestDepartment:

    @pytest.mark.django_db
    def test_create_department(self, department, user_db):

        assert department.name == 'Центр информационно-коммуникационных технологий'
        assert department.slug == 'cikt'
        assert department.short_name == 'ЦИКТ'
        assert department.phone == '+79169998877'
        assert department.email == 'cikt@kp11.ru'
        assert department.coordinate == 'г. Москва, Ленинградское шоссе, 13А'
        assert department.supervisor == department.supervisor
        assert department.supervisor.username == user_db.username

    @pytest.mark.django_db
    def test_get_absolute_url(self, department):
        expected_url = reverse('schedule_home', kwargs={'department_name': department.slug})
        assert department.get_absolute_url() == expected_url
