# Generated by Django 5.0 on 2024-09-12 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_platform', '0025_alter_stepforpoint_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='avatar',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='media/education_platform/images/', verbose_name='Обложка'),
        ),
        migrations.AlterField(
            model_name='stepforpoint',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='education_platform/video/', verbose_name='Загрузить видео'),
        ),
    ]