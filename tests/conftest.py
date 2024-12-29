import pytest
import datetime
from college.models import CustomPerson, Department, Auditory, SiteSettings
from educationpart.models import Studygroup, Profession
from reference.models import Reference, Type, Status
from docs.models import Category, Article


@pytest.fixture
def media_root(tmpdir, settings):
    """
    Подменяем MEDIA_ROOT на временную директорию, чтобы
    все загруженные файлы во время тестов сохранялись там.
    """
    settings.MEDIA_ROOT = tmpdir.strpath
    return settings.MEDIA_ROOT


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
            job_title='Преподаватель',
            is_teacher=True,
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
    user.save()
    yield user
    user.delete()


@pytest.fixture
def user_student(studygroup):
    user = CustomPerson.objects.create_user(
        username='sidorov_ma',
        password='Pa$$w0rd',
        first_name='Максим',
        last_name='Сидоров',
        middle_name='Александрович',
        email='sidorov@mail.ru',
        birthday=datetime.date(1997, 3, 1),
        job_title='Stydent',
        group=studygroup,
        is_active=True
    )
    user.save()
    yield user
    user.delete()


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
    yield department
    department.delete()


@pytest.fixture
def profession(department):
    prof = Profession(
        number='09.02.07',
        name='Информационные системы и программирование',
        shortname='ИСиП',
        department=department
    )
    prof.save()
    yield prof
    prof.delete()


@pytest.fixture
def studygroup(department, users, profession):
    group = Studygroup(
        name='ИСиП-41 (11 кл.)',
        slug='isip-41 (11 kl.)',
        admin_name='ИСиП2020-1',
        start_edu=datetime.date(2020, 9, 1),
        department=department,
        profession=profession
    )
    group.save()
    yield group
    group.delete()


@pytest.fixture
def auditory(department):
    auditory = Auditory(number='404', department=department)
    auditory.save()
    yield auditory
    auditory.delete()


@pytest.fixture
def reference_type_military():
    reference_type = Type(name='В военкомат', example='files/military.pdf')
    reference_type.save()
    yield reference_type
    reference_type.delete()


@pytest.fixture
def reference_status_create():
    reference_status = Status(name='Создан')
    reference_status.save()
    yield reference_status
    reference_status.delete()


@pytest.fixture
def reference_military(user_db, reference_type_military, reference_status_create):
    reference = Reference(
        user=user_db,
        type=reference_type_military,
        comment='Военный комиссариат Бабушкинского района СВАО города Москвы'
    )
    reference.save()
    yield reference
    reference.delete()


@pytest.fixture
def docs_category_visible():
    category = Category(
        name='Тестовый заголовок',
        slug='test_doc_category',
        description='Тестовое описание категории',
        icon='fa-icon-docs',
        is_active=True
    )
    category.save()
    yield category
    category.delete()


@pytest.fixture
def docs_article_visible(docs_category_visible):
    article = Article(
        category=docs_category_visible,
        name='Тестовая статья',
        slug='test_article',
        content='Тестовое содержание',
        is_active=True
    )
    article.save()
    yield article
    article.delete()
