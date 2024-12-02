# Generated by Django 5.0 on 2024-08-13 11:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_platform', '0011_trainingcoursecategory_trainingcoursesubcategory_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionForStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст вопроса')),
                ('number', models.IntegerField(verbose_name='Порядковый номер вопроса')),
            ],
            options={
                'verbose_name': 'Вопрос к блоку',
                'verbose_name_plural': 'Вопрос к блоку',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Тег')),
            ],
        ),
        migrations.RenameField(
            model_name='trainingcourse',
            old_name='name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='trainingcourseblock',
            name='text',
        ),
        migrations.RemoveField(
            model_name='trainingcourseblock',
            name='video',
        ),
        migrations.RemoveField(
            model_name='trainingcourseblock',
            name='video_url',
        ),
        migrations.AddField(
            model_name='trainingcourseblock',
            name='title',
            field=models.CharField(default='title', max_length=255, verbose_name='Заголовок блока'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='PointForTrainingBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название пункта')),
                ('number', models.FloatField(verbose_name='Номер пункта')),
                ('training_course_block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='points', to='education_platform.trainingcourseblock', verbose_name='Пункт обучения')),
            ],
            options={
                'verbose_name': 'Пункт блока обучения',
                'verbose_name_plural': 'Пункты блоков обучения',
            },
        ),
        migrations.RenameModel(
            old_name='Answer',
            new_name='AnswerForQuestion',
        ),
        migrations.AlterField(
            model_name='answerforquestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='education_platform.questionforstep'),
        ),
        migrations.CreateModel(
            name='StepForPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название шага')),
                ('number', models.FloatField(verbose_name='Номер шага')),
                ('text', models.TextField(verbose_name='Текст шага')),
                ('video_url', models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')),
                ('video', models.FileField(blank=True, null=True, upload_to='media/education_platform/video/', verbose_name='Загрузить видео')),
                ('point_for_training_block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='education_platform.pointfortrainingblock', verbose_name='Пункт обучения')),
            ],
            options={
                'verbose_name': 'Шаг для пункта обучения',
                'verbose_name_plural': 'Шаги для пунктов обучения',
            },
        ),
        migrations.AddField(
            model_name='questionforstep',
            name='step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='education_platform.stepforpoint', verbose_name='Вопрос для шага'),
        ),
        migrations.AddField(
            model_name='trainingcourse',
            name='tags',
            field=models.ManyToManyField(related_name='Теги', to='education_platform.tag'),
        ),
        migrations.DeleteModel(
            name='QuestionForTrainingCourseBlock',
        ),
    ]
