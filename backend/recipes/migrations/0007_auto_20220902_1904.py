# Generated by Django 3.2.2 on 2022-09-02 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_rename_ingredient_recipe_ingredients_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, default=None, help_text='Выберите картинку', upload_to='recipes/images/', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=16, unique=True, verbose_name='Цвет в HEX'),
        ),
    ]
