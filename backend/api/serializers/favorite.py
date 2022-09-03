from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.serializers.users import RecipeSubscriptionSerializer
from recipes.models import Favorite

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
        request = self.context.get('request')
        recipe_id = data['recipe'].id
        favorite_exists = Favorite.objects.filter(
            user=request.user,
            recipe__id=recipe_id
        ).exists()

        if request.method == 'GET' and favorite_exists:
            raise serializers.ValidationError(
                'Рецепт уже в избранном!'
            )

        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSubscriptionSerializer(
            instance.recipe,
            context=context).data
