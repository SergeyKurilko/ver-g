# Generated by Django 5.0 on 2024-03-02 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_alter_project_options_project_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
