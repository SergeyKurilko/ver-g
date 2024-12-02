# Generated by Django 5.0 on 2024-01-29 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_alter_service_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='preview',
            field=models.TextField(default='заполнить', verbose_name='Краткое описание услуги (для таблицы)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.TextField(verbose_name='Подробное описание услуги'),
        ),
    ]
