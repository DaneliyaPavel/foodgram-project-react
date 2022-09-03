from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers

from api.serializers.users import RecipeSubscriptionSerializer
from recipes.models import Favorite, Recipe

User = get_user_model()


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления рецепта в избранное.
    Доступно только авторизованному пользователю.
    """
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        if Favorite.objects.filter(
                user=self.context.get('request').user,
                recipe=data['recipe']
        ).exists():
            raise serializers.ValidationError({
                'status': 'Рецепт уже в избранном!'
            })
        return data

    def to_representation(self, instance):
        return RecipeSubscriptionSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data
