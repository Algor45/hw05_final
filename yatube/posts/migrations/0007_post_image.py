# Generated by Django 2.2.16 on 2022-09-02 13:04
"""Миграция."""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Миграция."""

    dependencies = [
        ('posts', '0006_auto_20220816_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='posts/', verbose_name='Картинка'),
        ),
    ]
