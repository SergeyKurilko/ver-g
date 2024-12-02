# Generated by Django 5.0 on 2024-08-12 16:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_platform', '0010_trainingcourse_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingCourseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Категория курсов')),
            ],
            options={
                'verbose_name': 'Категория курсов обучения',
                'verbose_name_plural': 'Категории курсов обучения',
            },
        ),
        migrations.CreateModel(
            name='TrainingCourseSubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Подкатегория курсов')),
            ],
            options={
                'verbose_name': 'Подкатегория курсов обучения',
                'verbose_name_plural': 'Подкатегории курсов обучения',
            },
        ),
        migrations.AddField(
            model_name='trainingcourse',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='education_platform.trainingcoursecategory', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='trainingcourse',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='education_platform.trainingcoursesubcategory', verbose_name='Подкатегория'),
        ),
    ]
