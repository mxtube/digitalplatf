import pytest


class TestAuditory:

    @pytest.mark.django_db
    def test_auditory_create(self, auditory):
        assert auditory.number == '404'
        assert auditory.department == auditory.department
        assert auditory.department.short_name == 'ЦИКТ'

    @pytest.mark.django_db
    def test_auditory_update(self, auditory):
        assert auditory.number == '404'
        auditory.number = '412а'
        auditory.save()
        assert auditory.number == '412а'
