# Generated by Django 2.2.6 on 2022-08-15 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20220816_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.TextField(help_text='Опишите группу', verbose_name='Описание группы'),
        ),
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(help_text='Укажите уникальный адрес', unique=True, verbose_name='Уникальный номер группы'),
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(help_text='Укажите название группы', max_length=200, verbose_name='Название группы'),
        ),
    ]
