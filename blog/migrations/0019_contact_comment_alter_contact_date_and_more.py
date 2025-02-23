# Generated by Django 5.0 on 2024-02-26 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_contact_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='comment',
            field=models.TextField(default='Мои комментарии', verbose_name='Мои комментарии'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата отправки'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='question',
            field=models.TextField(verbose_name='Комментарии'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Обработано'),
        ),
    ]
