# Generated by Django 5.0 on 2024-03-02 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0010_alter_servicecategory_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicecategory',
            name='name',
            field=models.CharField(max_length=250, unique=True, verbose_name='Категория услуг'),
        ),
    ]