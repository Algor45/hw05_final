import datetime as dt
import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.forms import PostForm
from posts.models import Group, Post

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsFormsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        post_author = User.objects.create(username='author')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            pub_date=dt.datetime.now(),
            author=post_author,
            group_id=0,
            pk=1,
        )
        cls.group = Group.objects.create(
            title='test_group',
            slug='test-slug',
            description='test_desk',
            pk=0
        )
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username='author')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Тестовый текст 2',
            'author': self.authorized_client,
            'image': uploaded,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(response,
                             reverse('posts:profile',
                                     kwargs={'username':
                                             self.post.author.username}),
                             msg_prefix='Ошибка проверки перенаправления')
        self.assertEqual(Post.objects.count(), posts_count + 1,
                         'Пост не был добавлен в базу')
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст 2',
                image='posts/small.gif'
            ).exists()
        )

    def test_edit_post_save(self):
        """Валидная форма изменяет запись в Post."""
        form_data = {
            'text': 'Тестовый текст 2',
            'author': self.authorized_client
        }

        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse('posts:post_detail',
                                               kwargs={'post_id':
                                                       self.post.pk}),
                             msg_prefix='Ошибка проверки перенаправления')
        self.assertEqual(response.context.get("post").text,
                         form_data.get('text'),
                         'text не был изменен')
