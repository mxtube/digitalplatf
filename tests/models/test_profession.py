import pytest


class TestProfessionModel:

    @pytest.mark.django_db
    def test_profession_creation(self, profession, department):

        assert profession.number == "09.02.07"
        assert profession.name == "Информационные системы и программирование"
        assert profession.shortname == "ИСиП"
        assert profession.department == department
        assert str(profession) == "09.02.07 Информационные системы и программирование"
