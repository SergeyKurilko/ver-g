# Generated by Django 5.0 on 2024-11-17 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_platform', '0045_promoindashboard'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursepack',
            name='published',
            field=models.BooleanField(default=False, verbose_name='Опубликовать'),
        ),
    ]
