# Generated by Django 5.0 on 2024-10-29 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_platform', '0042_student_edit_limit_alter_student_avatar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='edit_limit',
            field=models.PositiveIntegerField(default=2, verbose_name='Количество редактирований'),
        ),
    ]
