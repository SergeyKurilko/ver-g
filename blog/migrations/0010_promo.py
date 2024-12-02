# Generated by Django 5.0 on 2024-01-23 16:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_service_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Акция', max_length=5)),
                ('image', models.ImageField(upload_to='promo/service/')),
                ('service', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.service')),
            ],
            options={
                'verbose_name': 'Акция',
                'verbose_name_plural': 'Акция',
            },
        ),
    ]