import pytest
import datetime
from college.models import CustomPerson, Department, Auditory


@pytest.fixture
def users():
    return [
        CustomPerson(
            username='kuznetsovka',
            first_name='Кирилл',
            last_name='Кузнецов',
            middle_name='Александрович',
            email='kafomin@yandex.ru',
            birthday=datetime.date(1993, 10, 31),
            job_title='Engineer',
            is_active=True
        ),
        CustomPerson(
            username='utkina',
            first_name='Alex',
            last_name='Utkin',
            middle_name='',
            email='k31101993@yandex.ru',
            birthday=datetime.date(1998, 2, 8),
            job_title='System administrator',
            is_active=True
        )
    ]


@pytest.fixture
def department():
    supervisor = CustomPerson.objects.create(
        username='ivanovia',
        first_name='Иван',
        last_name='Иванов',
        middle_name='Иванович'
    )
    department = Department(
        name='Центр информационно-коммуникационных технологий',
        slug='cikt',
        short_name='ЦИКТ',
        phone='+79169998877',
        email='cikt@kp11.ru',
        coordinate='г. Москва, Ленинградское шоссе, 13А',
        supervisor=supervisor
    )
    department.save()
    return department


@pytest.fixture
def auditory(department):
    auditory = Auditory(number='404', department=department)
    auditory.save()
    return auditory
