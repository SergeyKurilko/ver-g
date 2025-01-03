# Generated by Django 5.0 on 2024-02-28 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_delete_promo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория статей', 'verbose_name_plural': 'Категории статей'},
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(upload_to='blog/images/%Y/%m/%d/', verbose_name='Изображение для карточки'),
        ),
    ]
