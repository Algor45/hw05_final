import datetime as dt
import shutil
import tempfile

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.models import Comment, Follow, Group, Post

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username='author')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        comment_author = User.objects.create(username='comment author')
        self.comment = Comment.objects.create(
            text='Тестовый комментарий',
            author=comment_author,
            post=self.post
        )
        cache.clear()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        post_author = User.objects.create(username='author')
        cls.author = Client()
        cls.author.force_login(post_author)
        cls.another_author = User.objects.create(username='another_author')
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile('small.gif', small_gif,
                                      content_type='image/gif')

        cls.post = Post.objects.create(
            text='Тестовый текст',
            pub_date=dt.datetime.now(),
            author=post_author,
            group_id=1,
            image=uploaded,
        )

        cls.group = Group.objects.create(
            title='test_group',
            slug='test-slug',
            description='test_desk'
        )

        cls.another_group = Group.objects.create(
            title='another_group',
            slug='another-slug',
            description='another_desk'
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def check_context(self, response, post):
        """Сверяем пост со страницы с постом в базе."""
        self.assertEqual(response.context.get('post').group_id,
                         post.group.pk,
                         'Ошибка в поле group')
        self.assertEqual(response.context.get('post').text, post.text,
                         'Ошибка в поле text')
        self.assertEqual(response.context.get('post').pk, post.pk,
                         'Передан неверный pk')
        self.assertEqual(response.context.get('post').pub_date, post.pub_date,
                         'Ошибка в поле pub_date')
        self.assertEqual(
            response.context.get('post').author.username,
            post.author.username,
            'Передан неверный author')
        self.assertTrue(response.context.get('post').image,
                        'не выводится изображение на странице поста')

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_posts', kwargs={'slug': self.group.slug}):
                'posts/group_list.html',
            reverse('posts:profile', kwargs={'username':
                                             self.post.author.username}):
                'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk}):
                'posts/post_detail.html',
            reverse('posts:post_create'):
                'posts/create_post.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}):
                'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template,
                                        f'Передан неверный шаблон {template}')

    def test_post_detail_correct_context(self):
        """ Проверка передача верных данных в post_detail"""
        response = (self.authorized_client.
                    get(reverse('posts:post_detail', kwargs={'post_id':
                                                             self.post.pk})))
        self.check_context(response, self.post)

    def test_index_show_correct_context(self):
        """Проверка правильности вывода постов на главную страницу."""
        response = (self.authorized_client.
                    get(reverse('posts:index')))
        self.check_context(response, self.post)

    def test_group_list_show_correct_context(self):
        """Проверка вывода верных постов на странице группы."""
        response = (self.authorized_client.
                    get(reverse('posts:group_posts',
                                kwargs={'slug': self.group.slug})))
        self.check_context(response, self.post)

    def test_profile_show_correct_context(self):
        """Проверка вывода верных постов на странице пользователя."""
        response = (self.authorized_client.
                    get(reverse('posts:profile',
                                kwargs={'username': 'author'})))
        self.check_context(response, self.post)

    def test_create_page_correct_context_fields(self):
        """Проверка вывода верных полей формы для create."""
        response = (self.authorized_client.
                    get(reverse('posts:post_create')))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected,
                                      f'ошибка при выводе поля {form_field}')

    def test_edit_page_correct_context_fields(self):
        """Проверка вывода верных полей формы для edit_page."""
        response = (self.authorized_client.
                    get(reverse('posts:post_edit',
                                kwargs={'post_id': self.post.pk})))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected,
                                      f'ошибка при выводе поля {form_field}')

    def test_edit_page_show_correct_field_values(self):
        """Проверка вывода значений в форму edit_page."""
        response = (self.authorized_client.
                    get(reverse('posts:post_edit', kwargs={'post_id':
                                                           self.post.pk})))
        self.assertEqual(response.context.get('post').text, self.post.text,
                         'ошибка при выводе значения text')
        self.assertEqual(
            response.context.get('post').group.title, self.post.group.title,
            'ошибка при выводе значения group')

    def test_comment_exists_base(self):
        """Проверка что комментарий имеется в базе."""
        form = {'text': 'Test comment',
                'post': self.post,
                'author': self.authorized_client}
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.pk}),
            data=form,
            follow=True)
        comment_created = response.context.get('post').comments.filter(
            post=self.post.pk,
            text='Test comment').get()
        comment_base = Comment.objects.filter(
            post=self.post.pk, text='Test comment').get()
        self.assertEqual(comment_base, comment_created,
                         'комментарий в базе отличается от созданного')

    def test_comment_adds(self):
        """Проверка что комментарий передается на страницу post_detail."""
        response = (self.authorized_client.
                    get(reverse('posts:post_detail', kwargs={'post_id':
                                                             self.post.pk})))
        self.assertEqual(response.context.get('post').comments.get(),
                         self.comment,
                         'Ошибка при передаче комментария в post_detail')

    def test_index_cache(self):
        """Проверка кэширования."""
        cached_post = Post.objects.create(
            author=self.another_author,
            text='Кэшированный тестовый текст поста'
        )
        response = (self.authorized_client.
                    get(reverse('posts:index')))
        self.assertIn(cached_post.text, response.content.decode(),
                      'Пост отсутствует на главной странице')
        cached_post.delete()
        self.assertIn(cached_post.text, response.content.decode(),
                      'Пост не был закэширован')
        cache.clear()
        response_cleared = (self.authorized_client.
                            get(reverse('posts:index')))
        self.assertNotIn(cached_post.text, response_cleared.content.decode(),
                         'Пост оcnался на главной странице после очистки кэша')


class PaginatorTests(TestCase):
    def setUp(self):
        self.user = User.objects.get(username='author')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        post_author = User.objects.create(username='author')
        cls.author = Client()
        cls.author.force_login(post_author)
        cls.group = Group.objects.create(
            title='test_group',
            slug='test-slug',
            description='test_desk'
        )
        number_of_posts = 13
        Post.objects.bulk_create(Post(text=f'Тестовый текст {number}',
                                      author=post_author,
                                      pub_date=dt.datetime.now(),
                                      group_id=1)
                                 for number in range(number_of_posts))

    def test_first_index_page_contains_ten_records(self):
        response = self.authorized_client.get(reverse('posts:index'))
        """Проверка что на 1ой странице главной 10 сообщений."""
        self.assertEqual(len(response.context['page_obj']), 10,
                         'Выведено неверное количество постов')

    def test_second_index_page_contains_three_records(self):
        """Проверка что на 2ой странице главной 3 сообщения."""
        response = self.authorized_client.get(reverse('posts:index')
                                              + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3,
                         'Выведено неверное количество постов')

    def test_first_group_page_contains_ten_records(self):
        """Проверка что на 1ой странице группы 10 сообщений."""
        response = self.authorized_client.get(
            reverse('posts:group_posts', kwargs={'slug': 'test-slug'}))
        self.assertEqual(len(response.context['page_obj']), 10,
                         'Выведено неверное количество постов')

    def test_second_group_page_contains_three_records(self):
        """Проверка что на 2ой странице группы 3 сообщения."""
        response = self.authorized_client.get(
            reverse('posts:group_posts',
                    kwargs={'slug': 'test-slug'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3,
                         'Выведено неверное количество постов')

    def test_first_profile_page_contains_ten_records(self):
        """Проверка что на 1ой странице профиля 10 сообщений."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': 'author'}))
        self.assertEqual(len(response.context['page_obj']), 10,
                         'Выведено неверное количество постов')

    def test_second_profile_page_contains_three_records(self):
        """Проверка что на 2ой странице профиля 3 сообщения."""
        response = self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': 'author'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3,
                         'Выведено неверное количество постов')


class FollowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author_followed = User.objects.create(username='author_first')
        cls.author_not_followed = User.objects.create(username='author_second')
        cls.current_user = User.objects.create(username='current_user')
        cls.group = Group.objects.create(
            title='test_group',
            slug='test-slug',
            description='test_desk'
        )
        cls.post_follow = Post.objects.create(
            text='Пост подписанного автора',
            pub_date=dt.datetime.now(),
            author=cls.author_followed,
            group_id=1
        )
        cls.post_not_follow = Post.objects.create(
            text='Пост не подписанного автора ',
            pub_date=dt.datetime.now(),
            author=cls.author_not_followed,
            group_id=1
        )
        cls.follow = Follow.objects.create(
            user=cls.current_user,
            author=cls.author_followed
        )

    def check_context(self, response, post):
        """Сверяем пост со страницы с новым постом."""
        response_post = response.context.get('page_obj')[0]
        self.assertEqual(response_post.group_id,
                         post.group.pk,
                         'Ошибка в поле group')
        self.assertEqual(response_post.text, post.text,
                         'Ошибка в поле text')
        self.assertEqual(response_post.pk, post.pk,
                         'Передан неверный pk')
        self.assertEqual(response_post.pub_date, post.pub_date,
                         'Ошибка в поле pub_date')
        self.assertEqual(
            response_post.author.username,
            post.author.username,
            'Передан неверный author')

    def setUp(self):
        self.authorized_user = Client()
        self.authorized_user.force_login(self.current_user)
        cache.clear()

    def test_new_post_shows_follow(self):
        """Проверка новый пост появляется если есть подписка на автора."""
        new_post = Post.objects.create(
            author=self.author_followed,
            text='Новый пост отслеживаемого автора',
            group_id=1
        )
        response = (self.authorized_user.
                    get(reverse('posts:follow_index')))
        self.assertIn(new_post, response.context.get('page_obj'),
                      'Поста отслеживаемого автора нет на странице')
        self.check_context(response, new_post)

    def test_new_post_hide_unfollow(self):
        """Новый пост не отображается если нет подписки на автора."""
        new_post = Post.objects.create(
            author=self.author_not_followed,
            text='Новый пост не отслеживаемого автора'
        )
        response = (self.authorized_user.
                    get(reverse('posts:follow_index')))
        self.assertTrue(Post.objects.filter(pk=new_post.pk).exists(),
                        'Пост существует в базе')
        self.assertNotIn(new_post, response.context.get('page_obj'),
                         'Выведен пост неотслеживаемого автора')

    def test_unfollow(self):
        """Проверка возможности отписаться."""
        self.authorized_user.get(reverse('posts:profile_unfollow',
                                         kwargs={'username':
                                                 self.author_followed}))
        followed_authors = Follow.objects.filter(user=self.current_user,
                                                 author=self.author_followed)
        self.assertEqual(followed_authors.count(), 0,
                         'Не удалось отписаться от автора ')

    def test_follow(self):
        """Проверка возможности подписаться."""
        self.authorized_user.get(reverse('posts:profile_follow',
                                         kwargs={'username':
                                                 self.author_not_followed}))
        followed_authors = Follow.objects.filter(user=self.current_user,
                                                 author=self.author_followed)
        self.assertEqual(followed_authors.count(), 1,
                         'Не удалось подписаться на автора')
