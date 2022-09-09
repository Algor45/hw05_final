from django.test import Client, TestCase


class CoreURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_tech_url_template_exists(self):
        """Страница 404 отдает кастомный шаблон."""
        response = self.guest_client.get('/rr/')
        self.assertTemplateUsed(response, 'core/404.html')
