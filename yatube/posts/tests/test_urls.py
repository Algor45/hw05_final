import datetime as dt
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from posts.models import Group, Post

User = get_user_model()


class PostsURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='user')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.unauth_response = {
            '': ['posts/index.html', HTTPStatus.OK],
            '/group/test-slug/': ['posts/group_list.html', HTTPStatus.OK],
            '/profile/author/': ['posts/profile.html', HTTPStatus.OK],
            '/posts/1/': ['posts/post_detail.html', HTTPStatus.OK],
            '/create/': ['posts/create_post.html', HTTPStatus.FOUND],
            '/posts/1/edit/': ['posts/create_post.html', HTTPStatus.FOUND],
            '/unexisting_page/': [None, HTTPStatus.NOT_FOUND]
        }

        cls.auth_response = {
            '': ['posts/index.html', HTTPStatus.OK],
            '/group/test-slug/': ['posts/group_list.html', HTTPStatus.OK],
            '/profile/author/': ['posts/profile.html', HTTPStatus.OK],
            '/posts/1/': ['posts/post_detail.html', HTTPStatus.OK],
            '/create/': ['posts/create_post.html', HTTPStatus.OK],
            '/posts/1/edit/': ['posts/create_post.html', HTTPStatus.FOUND],
            '/unexisting_page/': [None, HTTPStatus.NOT_FOUND]
        }

        cls.unauth_redirect = {
            '/create/': '/auth/login/?next=/create/',
            '/posts/1/edit/': '/auth/login/?next=/posts/1/edit/'
        }
        cls.auth_redirect = {
            '/posts/1/edit/': '/posts/1/'
        }

        user = User.objects.create_user(username='author')
        cls.author = Client()
        cls.author.force_login(user)
        cls.post = Post.objects.create(
            text='Тестовый текст',
            pub_date=dt.datetime.now(),
            author=user,
            group_id=1,
            pk=1
        )

        cls.group = Group.objects.create(
            title='test_group',
            slug='test-slug',
            description='test_desk',
            pk=1

        )

    def check_status_code_and_template(self, user, response_dict):
        for address, (template, status) in response_dict.items():
            response = user.get(address)
            self.assertEqual(response.status_code, status,
                             'проверьте что указаны верные адреса страниц')
            if response.status_code == HTTPStatus.OK:
                self.assertTemplateUsed(response, template,
                                        'проверьте названия шаблонов')

    def check_redirect(self, user, redirect_dict):
        for address, redirect_address in redirect_dict.items():
            with self.subTest(address=address):
                response = user.get(address, follow=True)
                self.assertRedirects(response, redirect_address,
                                     msg_prefix='Ошибка при перенаправлении')

    def test_status_code_and_template_auth(self):
        """ Проверка названия шаблонов и status code
            для авторизованного пользователя"""
        self.check_status_code_and_template(self.authorized_client,
                                            self.auth_response)

    def test_status_code_and_template_unauth(self):
        """ Проверка названия шаблонов и status code
            для неавторизованного пользователя"""
        self.check_status_code_and_template(self.guest_client,
                                            self.unauth_response)

    def test_redirect_unauth(self):
        """ Проверка перенаправления для авторизованного пользователя"""
        self.check_redirect(self.guest_client, self.unauth_redirect)

    def test_redirect_auth(self):
        """ Проверка перенаправления для неавторизованного пользователя"""
        if self.authorized_client != PostsURLTests.author:
            self.check_redirect(self.authorized_client, self.auth_redirect)

    def test_comment_unauth_redirect(self):
        """ Проверка что неавторизаванного пользователя перенаправляет
            на страниу логина при попытке добавить комментарий"""
        response = self.guest_client.get('/posts/1/comment', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/posts/1/comment/',
                             status_code=301, target_status_code=200)
