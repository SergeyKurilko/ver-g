# Generated by Django 5.0 on 2024-08-09 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_platform', '0005_trainingcourse_is_free_trainingcourse_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingcourseblock',
            name='video_url',
            field=models.URLField(blank=True, null=True, verbose_name='Видео'),
        ),
    ]
