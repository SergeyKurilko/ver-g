# Generated by Django 5.0 on 2024-11-25 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_platform', '0047_alter_trainingcourse_difficulty_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursepack',
            name='meta_description',
            field=models.CharField(default='meta description example', max_length=255, verbose_name='Description meta tag'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trainingcourse',
            name='meta_description',
            field=models.CharField(default='meta description example', max_length=255, verbose_name='Description meta tag'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coursepack',
            name='title',
            field=models.CharField(max_length=255, unique=True, verbose_name='Название пакета курсов'),
        ),
    ]
