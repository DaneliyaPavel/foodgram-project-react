import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Загрузка ингредиентов в базу данных из csv"

    def handle(self, *args, **kwargs):
        with open(
                f'{settings.BASE_DIR}/data/ingredients.csv',
                'r',
                encoding='utf-8'
        ) as file:
            ingredients = csv.reader(file, delimiter=',')
            for ingredient in ingredients:
                if len(ingredient) == 2:
                    Ingredient.objects.get_or_create(
                        name=ingredient[0], measurement_unit=ingredient[1]
                    )

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена'))
        return 'OK'
