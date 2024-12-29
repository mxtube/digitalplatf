import pytest
from django.urls import reverse


class TestViewAccess:

    @pytest.mark.parametrize('url_path', ['homepage', 'password_reset', 'docs_home'])
    @pytest.mark.django_db
    def test_visible_page_for_anonymous_user(self, client, url_path):
        """ Тест проверяет, что анонимный пользователь может открыть страницу (ожидается статус 200) """
        url = reverse(url_path)
        response = client.get(url)
        assert response.status_code == 200

    @pytest.mark.parametrize('url_path', ['profile', 'edit_profile', 'suggestion', 'reference_home'])
    @pytest.mark.django_db
    def test_redirect_to_login_view_for_anonymous_user(self, client, url_path):
        """
        Тест проверяет, что анонимного пользователя
        перенаправят на страницу логина при попытке открыть страницу
        (ожидается статус код 302 и login в url)
        """
        url = reverse(url_path)
        response = client.get(url)
        assert response.status_code == 302
        assert 'login' in response.url

    @pytest.mark.parametrize('url_path', ['homepage', 'profile', 'edit_profile', 'suggestion', 'docs_home'])
    @pytest.mark.django_db
    def test_present_view_for_authenticated_user(self, client, django_user_model, url_path):
        """
        Тест проверяет, что авторизованный пользователь
        может открыть страницу (ожидается статус 200)
        """
        django_user_model.objects.create_user(username='testuser', password='testpassword')
        client.login(username='testuser', password='testpassword')

        url = reverse(url_path)
        response = client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_password_reset_view_authenticated_user(self, client, django_user_model):
        """
        Тест проверяет, что авторизованного пользователя
        перенаправят на страницу профиля при попытке открыть /password-reset/
        """
        django_user_model.objects.create_user(username='testuser', password='testpassword')
        client.login(username='testuser', password='testpassword')

        url = reverse('password_reset')
        response = client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_docs_article_visible_view_anonymous_user(self, client, docs_article_visible):
        """
        Тест проверяет, что анонимный пользователь
        может открыть страницу с детальной информацией документации (ожидается статус 200)
        """
        url = reverse('docs_article', kwargs={
            'category_name': docs_article_visible.category.slug,
            'article_name': docs_article_visible.slug
        })
        response = client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_docs_article_visible_view_authenticated_user(self, client, django_user_model, docs_article_visible):
        """
        Тест проверяет, что авторизованный пользователь
        может открыть страницу с детальной информацией документации (ожидается статус 200)
        """
        django_user_model.objects.create_user(username='testuser', password='testpassword')
        client.login(username='testuser', password='testpassword')

        url = reverse('docs_article', kwargs={
            'category_name': docs_article_visible.category.slug,
            'article_name': docs_article_visible.slug
        })
        response = client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_no_visible_and_no_found_docs_article_view_anonymous_user(self, client, docs_article_visible):
        """
        Тест проверяет, что анонимный пользователь
        не может открыть страницу с детальной информацией документации которая не создана или скрыта
        (ожидается статус 404)
        """
        url = reverse('docs_article', kwargs={
            'category_name': 'kategorya',
            'article_name': 'no_created'
        })
        response = client.get(url)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_no_visible_and_no_found_docs_article_view_authenticated_user(self, client, django_user_model,
                                                                          docs_article_visible):
        """
        Тест проверяет, что авторизованный пользователь
        не может открыть страницу с детальной информацией документации которая не создана или скрыта
        (ожидается статус 404)
        """
        django_user_model.objects.create_user(username='testuser', password='testpassword')
        client.login(username='testuser', password='testpassword')

        url = reverse('docs_article', kwargs={
            'category_name': 'kategorya',
            'article_name': 'no_created'
        })
        response = client.get(url)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_reference_view_authenticated_user(self, client, user_student):
        """
        Тест проверяет, что авторизованный пользователь студент
        может открыть главную страницу документации (ожидается статус 200)
        """

        client.login(username=user_student.username, password='Pa$$w0rd')

        url = reverse('reference_home')
        response = client.get(url)
        assert response.status_code == 200
