# Generated by Django 5.0 on 2024-03-02 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0009_alter_orderforservice_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicecategory',
            name='slug',
            field=models.SlugField(max_length=250, unique=True),
        ),
    ]