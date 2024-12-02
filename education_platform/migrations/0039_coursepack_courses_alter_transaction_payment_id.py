# Generated by Django 5.0 on 2024-10-15 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_platform', '0038_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursepack',
            name='courses',
            field=models.ManyToManyField(to='education_platform.trainingcourse'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='payment_id',
            field=models.CharField(max_length=100, unique=True, verbose_name='ID платежа от yookassa'),
        ),
    ]
