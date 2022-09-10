"""Write your Core app tests here."""
from django.test import Client, TestCase


class CoreURLTests(TestCase):
    """Тестрирует приложение Core."""

    def setUp(self):
        """Устанавливает значения перед каждым тестом."""
        self.guest_client = Client()

    def test_404_url_template_exists(self):
        """Страница 404 отдает кастомный шаблон."""
        response = self.guest_client.get('/rr/')
        self.assertTemplateUsed(response, 'core/404.html')
