# Generated by Django 5.0 on 2024-02-26 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_contact_comment_alter_contact_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='question',
            field=models.TextField(verbose_name='Комментарии посетителя'),
        ),
    ]