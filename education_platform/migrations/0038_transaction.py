# Generated by Django 5.0 on 2024-10-12 05:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_platform', '0037_coursepack'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Сумма платежа')),
                ('payment_id', models.CharField(max_length=100, unique=True, verbose_name='ID платежа от youkassa')),
                ('status', models.CharField(max_length=50, verbose_name='Статус платежа')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания платежа')),
                ('product_type', models.CharField(choices=[('course', 'Курс'), ('course_pack', 'Пакет курсов')], max_length=20, verbose_name='Тип продукта')),
                ('product_id', models.PositiveIntegerField(verbose_name='ID продукта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
            },
        ),
    ]