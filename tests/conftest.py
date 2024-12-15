import pytest
import datetime
from college.models import CustomPerson, Department, Auditory, SiteSettings
from reference.models import Reference, Type, Status


@pytest.fixture
def site_settings():
    settings = SiteSettings.objects.create(
        site_name='Государственное автономное профессиональное образовательное учреждение города Москвы Колледж предпринимательства №11',  # noqa E501
        short_site_name='ГАПОУ КП №11',
        logotype='logo.png',
        description='Образовательная организация',
        contact_description='Мы находимся по адресу: г. Москва, Онежская дом 3',
        phone='+74954445566',
        email='support@kp11.ru',
        address='129344, г. Москва, Проспект мира д.1',
        vk_link='https://vk.com/',
        youtube_link='https://youtube.com/',
        odnoklassniki_link='https://ok.ru/',
        dzen_link='https://dzen.ru/',
        telegram_link='https://t.me/',
        whatsapp_link='https://whatsapp.ru/'
    )
    settings.save()
    return settings


@pytest.fixture
def users():
    return [
        CustomPerson(
            username='kuznetsovka',
            password='Pa$$w0rd',
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
            password='Pa$$w0rd',
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
def user_db():
    user = CustomPerson.objects.create_user(
        username='petrovsa',
        password='Pa$$w0rd',
        first_name='Сергей',
        last_name='Петров',
        middle_name='Алексеевич',
        email='kafomin@yandex.ru',
        birthday=datetime.date(1997, 3, 1),
        job_title='Stydent',
        is_active=True
    )
    return user


@pytest.fixture
def department(user_db):
    department = Department(
        name='Центр информационно-коммуникационных технологий',
        slug='cikt',
        short_name='ЦИКТ',
        phone='+79169998877',
        email='cikt@kp11.ru',
        coordinate='г. Москва, Ленинградское шоссе, 13А',
        supervisor=user_db
    )
    department.save()
    return department


@pytest.fixture
def auditory(department):
    auditory = Auditory(number='404', department=department)
    auditory.save()
    return auditory


@pytest.fixture
def reference_type_military():
    reference_type = Type(name='В военкомат', example='files/military.pdf')
    reference_type.save()
    return reference_type


@pytest.fixture
def reference_status_create():
    reference_status = Status(name='Создан')
    reference_status.save()
    return reference_status


@pytest.fixture
def reference_military(user_db, reference_type_military, reference_status_create):
    reference = Reference(
        user=user_db,
        type=reference_type_military,
        comment='Военный комиссариат Бабушкинского района СВАО города Москвы'
    )
    reference.save()
    return reference
