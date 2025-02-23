# Generated by Django 5.0 on 2024-01-29 05:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_servicecategory_service_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='services', to='service.servicecategory', verbose_name='Категория услуги'),
        ),
    ]
