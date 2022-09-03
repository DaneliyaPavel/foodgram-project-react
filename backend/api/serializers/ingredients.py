from rest_framework import serializers

from recipes.models import Ingredient, IngredientInRecipe


class IngredientListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода ингредиентов.
    """

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода
    количества ингредиентов в рецепте.
    """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class AddIngredientInRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления ингредиентов
    в рецепт.
    """
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')
