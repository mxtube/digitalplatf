import pytest


class TestReference:

    @pytest.mark.django_db
    def test_reference_create(self, reference_military):
        assert reference_military.user.get_fullname == 'Петров Сергей Алексеевич'
        assert reference_military.type.name == 'В военкомат'
        assert reference_military.comment == 'Военный комиссариат Бабушкинского района СВАО города Москвы'
        assert reference_military.status.name == 'Создан'
        reference_military.delete()

    @pytest.mark.django_db
    def test_reference_type(self, reference_type_military):
        assert reference_type_military.name == 'В военкомат'
        assert reference_type_military.example.url == '/media/files/military.pdf'
        reference_type_military.delete()
