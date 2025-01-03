# Generated by Django 5.0 on 2024-11-15 06:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_platform', '0043_alter_student_edit_limit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trainingcourse',
            options={'ordering': ['-priority'], 'verbose_name': 'Курс обучения', 'verbose_name_plural': 'Курсы обучения'},
        ),
        migrations.AddField(
            model_name='trainingcourse',
            name='priority',
            field=models.PositiveIntegerField(default=1, verbose_name='Приоритет очереди'),
        ),
        migrations.AddField(
            model_name='trainingcourse',
            name='published',
            field=models.BooleanField(default=False, verbose_name='Опубликовать'),
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=8, verbose_name='code')),
                ('sale_value', models.PositiveIntegerField(verbose_name='Скидка в процентах')),
                ('validity_period', models.DateField(blank=True, default=None, null=True, verbose_name='Срок действия')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promo_codes', to='education_platform.trainingcourse')),
            ],
            options={
                'verbose_name': 'Промо код',
                'verbose_name_plural': 'Промо коды',
            },
        ),
        migrations.AddField(
            model_name='transaction',
            name='promo_code',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='promo_codes', to='education_platform.promocode', verbose_name='Промокод'),
        ),
    ]
