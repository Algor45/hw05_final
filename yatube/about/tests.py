"""Write your About app tests here."""

from django.test import Client, TestCase


class AboutURLTests(TestCase):
    """Тесты страниц приложения About."""

    def setUp(self):
        """Устанавливает значения перед каждым тестом."""
        self.guest_client = Client()

    def test_tech_url_exists_at_desired_location(self):
        """Страница /tech/ доступна любому пользователю."""
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200)

    def test_task_author_url_exists_at_desired_location(self):
        """Страница /author/ доступна любому пользователю."""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200)

    def test_tech_url_template_exists(self):
        """Страница /tech/ использует верный шаблон."""
        response = self.guest_client.get('/about/tech/')
        self.assertTemplateUsed(response, 'about/tech.html')

    def test_task_author_url_template_exists(self):
        """Страница /author/ использует верный шаблон."""
        response = self.guest_client.get('/about/author/')
        self.assertTemplateUsed(response, 'about/author.html')
