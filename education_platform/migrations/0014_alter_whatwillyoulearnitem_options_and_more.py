# Generated by Django 5.0 on 2024-08-14 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_platform', '0013_whatwillyoulearnitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='whatwillyoulearnitem',
            options={'verbose_name': 'Строка для списка "Чему вы научитесь?"', 'verbose_name_plural': 'Строки для списка "Чему вы научитесь?"'},
        ),
        migrations.AddField(
            model_name='trainingcourse',
            name='about_author',
            field=models.TextField(default='about authoe', verbose_name='Об авторе курса'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trainingcourse',
            name='full_description',
            field=models.TextField(default='full description', verbose_name='Полное описание курса обучения'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trainingcourse',
            name='who_is_this_course_for',
            field=models.TextField(default='for whom', verbose_name='Для кого этот курс'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trainingcourse',
            name='description',
            field=models.TextField(verbose_name='Краткое описание курса обучения'),
        ),
    ]