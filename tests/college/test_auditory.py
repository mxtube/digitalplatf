import pytest


class TestAuditory:

    @pytest.mark.django_db
    def test_auditory_create(self, auditory):
        assert auditory.number == '404'
        assert auditory.department == auditory.department
        assert auditory.department.short_name == 'ЦИКТ'
