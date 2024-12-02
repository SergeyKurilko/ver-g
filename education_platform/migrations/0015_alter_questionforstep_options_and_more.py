# Generated by Django 5.0 on 2024-08-15 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_platform', '0014_alter_whatwillyoulearnitem_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questionforstep',
            options={'verbose_name': 'Вопрос к шагу', 'verbose_name_plural': 'Вопросы к шагу'},
        ),
        migrations.AddField(
            model_name='trainingcourse',
            name='difficulty',
            field=models.CharField(choices=[('1', 'Начальный уровень'), ('2', 'Средний уровень'), ('3', 'Высокий уровень')], default='2', max_length=1),
        ),
    ]
