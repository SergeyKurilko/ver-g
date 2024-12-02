# Generated by Django 5.0 on 2024-09-14 07:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_platform', '0027_alter_student_avatar'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentForStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('published', models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Отредактировано')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='education_platform.commentforstep')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='education_platform.stepforpoint', verbose_name='Шаг')),
            ],
        ),
    ]