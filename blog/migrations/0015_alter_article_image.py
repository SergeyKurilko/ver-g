# Generated by Django 5.0 on 2024-02-22 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_alter_promo_service_delete_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(upload_to='blog/images/%Y/%m/%d/', verbose_name='Изображение (280px*350px)'),
        ),
    ]