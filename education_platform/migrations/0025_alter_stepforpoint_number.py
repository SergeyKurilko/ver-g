# Generated by Django 5.0 on 2024-09-06 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_platform', '0024_alter_pointfortrainingblock_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stepforpoint',
            name='number',
            field=models.PositiveIntegerField(verbose_name='Номер шага'),
        ),
    ]