# Generated by Django 5.0 on 2023-12-26 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_article_options_article_preview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='preview',
            field=models.TextField(verbose_name='Описание статьи'),
        ),
    ]