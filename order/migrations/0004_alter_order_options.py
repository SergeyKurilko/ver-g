# Generated by Django 4.1 on 2024-03-12 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_exactly_name_application'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-pk'], 'verbose_name': 'Заявка от клиента', 'verbose_name_plural': 'Заявки от клиентов'},
        ),
    ]
