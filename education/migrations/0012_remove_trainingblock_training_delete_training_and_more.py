# Generated by Django 5.0 on 2024-11-29 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0011_training_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainingblock',
            name='training',
        ),
        migrations.DeleteModel(
            name='Training',
        ),
        migrations.DeleteModel(
            name='TrainingBlock',
        ),
    ]
