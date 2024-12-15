import pytest


class TestSiteSettings:

    @pytest.mark.django_db
    def test_site_settings_create(self, site_settings):

        assert site_settings.site_name == 'Государственное автономное профессиональное образовательное учреждение города Москвы Колледж предпринимательства №11'  # noqa E501
        assert site_settings.short_site_name == 'ГАПОУ КП №11'
        assert site_settings.logotype.url == '/media/logo.png'
        assert site_settings.description == 'Образовательная организация'
        assert site_settings.contact_description == 'Мы находимся по адресу: г. Москва, Онежская дом 3'
        assert site_settings.phone == '+74954445566'
        assert site_settings.email == 'support@kp11.ru'
        assert site_settings.address == '129344, г. Москва, Проспект мира д.1'
        assert site_settings.vk_link == 'https://vk.com/'
        assert site_settings.odnoklassniki_link == 'https://ok.ru/'
        assert site_settings.dzen_link == 'https://dzen.ru/'
        assert site_settings.telegram_link == 'https://t.me/'
        assert site_settings.whatsapp_link == 'https://whatsapp.ru/'
        settings.delete()

    def test_social_network(self):
        pass
