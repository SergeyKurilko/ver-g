# Generated by Django 4.1 on 2024-03-09 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_alter_project_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='meta_description',
            field=models.CharField(default='вписать meta description', max_length=200, verbose_name='meta description'),
        ),
    ]