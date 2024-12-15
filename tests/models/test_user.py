import pytest
from college.models import CustomPerson

from datetime import date


class TestCustomPerson:

    @pytest.mark.django_db
    def test_custom_person_create(self):
        """ Тест на создание нового пользователя """
        user = CustomPerson.objects.create(
            username="testuser",
            first_name="John",
            last_name="Doe",
            middle_name="Smith",
            email="test@example.com",
            birthday=date(1990, 1, 1),
            job_title="Engineer",
            is_teacher=True
        )

        assert user.username == "testuser"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.middle_name == "Smith"
        assert user.email == "test@example.com"
        assert user.birthday == date(1990, 1, 1)
        assert user.job_title == "Engineer"
        assert user.is_teacher is True

    @pytest.mark.django_db
    def test_get_fullname(self):
        """ Тест метода получения полного имени пользователя """
        user = CustomPerson.objects.create(
            username="testuser",
            first_name="John",
            last_name="Doe",
            middle_name="Smith"
        )
        assert user.get_fullname == "Doe John Smith"

    @pytest.mark.django_db
    @pytest.mark.parametrize('username, first_name, last_name, middle_name, expected', [
        ('kuznetsovka', 'Кирилл', 'Кузнецов', 'Александрович', 'Кузнецов К.А.'),
        ('klimovichsv', 'Segey', 'Klimovich', 'Vladimirovich', 'Klimovich S.V.'),
        ('utkina', 'Aleksandr', 'Utkin', '', 'Utkin A.'),
    ])
    def test_get_name_initials(self, username, first_name, last_name, middle_name, expected):
        """ Тест метода получения фамилии с инициалами пользователя """
        user = CustomPerson.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name
        )
        assert user.get_name_initials() == expected

    @pytest.mark.django_db
    @pytest.mark.parametrize('username, first_name, last_name, middle_name', [
        ('IvanovIA', 'Ivan', 'Ivanov', 'Aleksandrovich'),
        ('ZuevI', 'Zuev', 'Igor', '')
    ])
    def test_get_user_by_fio(self, username, first_name, last_name, middle_name):
        """ Тест статического метода получения пользователя по ФИО """
        user = CustomPerson.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name
        )
        full_name = user.get_fullname
        found_user = CustomPerson.get_user_by_fio(full_name)

        assert found_user is not None
        assert found_user == user
