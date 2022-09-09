from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Модель сообщества"""
    title: str = models.CharField(max_length=200,
                                  verbose_name='Название группы',
                                  help_text='Укажите название группы')
    slug: str = models.SlugField(unique=True,
                                 verbose_name='Уникальный номер группы',
                                 help_text='Укажите уникальный адрес')
    description: str = models.TextField(verbose_name='Описание группы',
                                        help_text='Опишите группу')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    """Модель записей """
    text: str = models.TextField(verbose_name='Текст поста',
                                 help_text='Содержание поста')
    pub_date: datetime = models.DateTimeField(auto_now_add=True,
                                              verbose_name='Дата публикации',
                                              help_text='Укажите дату')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        help_text='Укажите автора'
    )
    group = models.ForeignKey(
        Group,
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Укажите группу'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """ Модель комментариев"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
        help_text='Ввод комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
        help_text='Укажите автора комментария'
    )
    text: str = models.TextField(verbose_name='Текст коментария',
                                 help_text='Комментарий')
    created: datetime = models.DateTimeField(auto_now_add=True,
                                             verbose_name='Дата подписки')


class Follow(models.Model):
    """Модель подписок"""
    user = models.ForeignKey(
        User,
        blank=True, null=True,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        blank=True, null=True,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Следят',
    )
