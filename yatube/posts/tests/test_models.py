from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_correct_names(self):
        """Проверка, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        expected_name = str(post)
        self.assertEqual(expected_name, post.text[:15],
                         'неверное отображение __str__ поста')

        group = PostModelTest.group
        expected_name = str(group)
        self.assertEqual(expected_name, group.title,
                         'неверное отображение __str__ группы')

    def test_Post_verbose_name(self):
        """ Проверка verbose_name полей модели Post"""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'group': 'Группа',
            'author': 'Автор'
        }
        for field, expected_value in field_verboses.items():
            self.assertEqual(post._meta.get_field(field).verbose_name,
                             expected_value)

    def test_Post_help_text(self):
        """ Проверка help_text полей модели Post"""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Содержание поста',
            'pub_date': 'Укажите дату',
            'group': 'Укажите группу',
            'author': 'Укажите автора'
        }
        for field, expected_value in field_help_texts.items():
            self.assertEqual(post._meta.get_field(field).help_text,
                             expected_value)

    def test_Group_verbose_name(self):
        """ Проверка verbose_name полей модели Group"""
        group = PostModelTest.group
        field_verboses = {
            'title': 'Название группы',
            'slug': 'Уникальный номер группы',
            'description': 'Описание группы'
        }
        for field, expected_value in field_verboses.items():
            self.assertEqual(group._meta.get_field(field).verbose_name,
                             expected_value)

    def test_Group_help_text(self):
        """ Проверка help_text полей модели Group"""
        group = PostModelTest.group
        field_help_texts = {
            'title': 'Укажите название группы',
            'slug': 'Укажите уникальный адрес',
            'description': 'Опишите группу'
        }
        for field, expected_value in field_help_texts.items():
            self.assertEqual(group._meta.get_field(field).help_text,
                             expected_value)
