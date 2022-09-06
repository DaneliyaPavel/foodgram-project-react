# Generated by Django 3.2.2 on 2022-09-03 19:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0007_auto_20220902_1904'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ['-created'], 'verbose_name': 'Корзина', 'verbose_name_plural': 'Корзины'},
        ),
        migrations.AlterModelOptions(
            name='favorite',
            options={'ordering': ['-created'], 'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранные'},
        ),
        migrations.AlterModelManagers(
            name='recipe',
            managers=[
                ('recipe_queryset', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата публикации'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cart',
            name='is_in_shopping_cart',
            field=models.BooleanField(default=False, verbose_name='В корзине покупок'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата публикации'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='favorite',
            name='is_favorited',
            field=models.BooleanField(default=False, verbose_name='В избранном'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_recipe', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]