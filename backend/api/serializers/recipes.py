from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.serializers.ingredients import (AddIngredientInRecipeSerializer,
                                         IngredientInRecipeSerializer)
from api.serializers.tags import TagListSerializer
from api.serializers.users import CustomUserSerializer
from recipes.models import (
    Cart, Ingredient, IngredientInRecipe,
    Recipe, Tag, Favorite
)


class RecipeListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения
    списка рецептов.
    """
    tags = TagListSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        depth = 1
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        """
        Проверка на вхождение в список избранного.
        """
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user,
                                       recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """
        Проверка на вхождение в корзину.
        """
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Cart.objects.filter(user=request.user,
                                   recipe=obj).exists()

    @staticmethod
    def get_ingredients(obj):
        ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(
            ingredients,
            many=True
        ).data


class RecipeCreateSerializer(serializers.ModelSerializer):
    """
    Cериализатор для создания и/или редактирования рецепта.
    """
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = AddIngredientInRecipeSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        if not ingredients:
            raise serializers.ValidationError('Добавьте ингредиент')
        elif not tags:
            raise serializers.ValidationError('Добавьте тег')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        ingredient_list = [
            IngredientInRecipe(
                recipe=recipe,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
            for ingredient in ingredients
        ]
        IngredientInRecipe.objects.bulk_create(ingredient_list)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        instance = super().update(instance, validated_data)
        if tags:
            instance.tags.set(tags)
        if ingredients:
            instance.ingredients.clear()
            ingredient_list = [
                IngredientInRecipe(
                    recipe=instance,
                    ingredient=ingredient.get('id'),
                    amount=ingredient.get('amount')
                )
                for ingredient in ingredients
            ]
            IngredientInRecipe.objects.bulk_create(ingredient_list)
        return instance

    def validate(self, data):
        ingredient_data = self.initial_data.get('ingredients')
        name = data.get('name')
        if ingredient_data:
            checked_ingredients = set()
            for ingredient in ingredient_data:
                ingredient_obj = get_object_or_404(
                    Ingredient, id=ingredient['id']
                )
                amount = data.get('ingredients')
                if [item for item in amount if item['amount'] < 1]:
                    raise serializers.ValidationError({
                        'amount':
                            'Убедитесь, что значение больше либо равно 1.'
                    })
                if ingredient_obj in checked_ingredients:
                    raise serializers.ValidationError('дубликат ингредиента')
                checked_ingredients.add(ingredient_obj)
                cooking_time = data.get('cooking_time')
                if cooking_time < 1:
                    raise serializers.ValidationError({
                        'cooking_time':
                            'Убедитесь, что значение больше либо равно 1.'
                    })
                if len(name) > 200:
                    raise serializers.ValidationError({
                        'name':
                            'Название рецепта не должно превышать 200 символов'
                    })
        return data

    def to_representation(self, recipe):
        return RecipeListSerializer(
            recipe,
            context={'request': self.context.get('request')}).data
