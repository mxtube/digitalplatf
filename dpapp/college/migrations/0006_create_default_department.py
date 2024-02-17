from django.db import migrations
from college.models import Department


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0005_auditory'),
        ('college', '0004_department'),
    ]

    def create_default_department(apps, schema_editor):

        obj = Department.objects.bulk_create(
            [
                Department(name='Центр аудиовизуальных технологий', short_name='ЦАВТ', phone='74950001122', coordinate='Москва, Онежская дом 3', supervisor_id=2),
                Department(name='Центр алмазных технологий и геммологии', short_name='ЦАТиГ', phone='74950001122', coordinate='Москва, Онежская дом 3', supervisor_id=2),
                Department(name='Центр информационно-коммуникационных технологий', short_name='ЦИКТ', phone='74950001122', coordinate='Москва, Онежская дом 3', supervisor_id=2),
                Department(name='Центр медицинской техники оптики', short_name='ЦМТиО', phone='74950001122', coordinate='Москва, Онежская дом 3', supervisor_id=2),
                Department(name='Центр предпринимательства и развития бизнеса', short_name='ЦПиРБ', phone='74950001122', coordinate='Москва, Онежская дом 3', supervisor_id=2),
                Department(name='Центр торгово-экономических компетенций', short_name='ЦТЭК', phone='74950001122', coordinate='Москва, Онежская дом 3', supervisor_id=2)
            ]
        )

    operations = [migrations.RunPython(create_default_department),]
