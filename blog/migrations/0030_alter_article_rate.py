# Generated by Django 5.0 on 2024-07-31 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0029_article_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='rate',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Рейтинг статьи'),
        ),
    ]
