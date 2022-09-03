from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from core.models import TimeStampedModel
from core.validators import slug_validation

User = get_user_model()


class Ingredient(models.Model):
    """
    Модель ингредиентов.
    Все поля обязательны для заполнения.
    """
    name: str = models.CharField(
        blank=False,
        null=False,
        db_index=True,
        max_length=200,
        verbose_name='Название'
    )
    measurement_unit: str = models.CharField(
        blank=False,
        null=False,
        max_length=20,
        verbose_name='Единица измерения'
    )

    class Meta:
        db_table = 'ingredients'
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return "{}, {}".format(self.name, self.measurement_unit)


class Tag(models.Model):
    """
    Модель тега.
    Цвет в формате HEX-кода.
    Все поля обязательны для заполнения.
    """
    name: str = models.CharField(
        null=False,
        blank=False,
        unique=True,
        max_length=200,
        verbose_name='Название'
    )
    color: str = models.CharField(
        max_length=16,
        unique=True,
        verbose_name='Цвет в HEX'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[slug_validation],
        verbose_name='Уникальный слаг'
    )

    class Meta:
        db_table = 'tags'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(TimeStampedModel):
    """
    Модель рецепта.
    Ингредиент и тег - множественные поля,
    с выбором из предустановленного списка.
    Все поля обязательны для заполнения.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_recipe',
        verbose_name='Автор публикации'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/images/',
        blank=True,
        default=None,
        help_text='Выберите картинку'
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
        help_text='Введите текст рецепта',
        blank=False,
        null=False
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientInRecipe",
        verbose_name='Ингредиент'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipe_tag',
        verbose_name='Тег'
    )
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1, 'Значение не должно быть меньше 1')],
        verbose_name='Время приготовления (в минутах)',
    )

    class Meta:
        db_table = 'recipes'
        ordering = ['-created']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(TimeStampedModel):
    """
    Модель количества ингредиентов в рецепте.
    """
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1, 'Значение не должно быть меньше 1')],
        verbose_name='Количество ингредиента',
        help_text='Введите количество ингредиента'
    )

    class Meta:
        db_table = 'ingredients_in_recipe'
        verbose_name = "Количество ингредиентов"
        verbose_name_plural = "Количество ингредиентов"
        constraints = (
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient'
            ),
        )

    def __str__(self):
        return f'{self.recipe}: {self.ingredient} – {self.amount}'


class Favorite(TimeStampedModel):
    """
    Модель избранных рецептов у пользователя.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites_user',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites_recipe',
        verbose_name='Рецепт',
    )

    class Meta:
        db_table = 'favorite'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite')
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном пользователя {self.user}'


class Cart(TimeStampedModel):
    """
    Модель списка покупок пользователя.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_user',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart_recipe',
        verbose_name='Рецепт',
    )

    class Meta:
        db_table = 'cart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_cart')
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в корзине пользователя {self.user}'
