# Generated by Django 5.0 on 2025-01-08 17:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_platform', '0050_alter_trainingcourse_signature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='promo_code',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='promo_codes', to='education_platform.promocode', verbose_name='Промокод'),
        ),
    ]
