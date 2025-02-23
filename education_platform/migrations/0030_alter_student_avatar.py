# Generated by Django 5.0 on 2024-09-15 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_platform', '0029_alter_student_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='avatar',
            field=models.ImageField(blank=True, default='static/education_platform/common_icons/blank_avatar.svg', null=True, upload_to='education_platform/student/avatars/', verbose_name='Обложка'),
        ),
    ]
