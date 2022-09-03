from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.serializers.users import RecipeSubscriptionSerializer
from recipes.models import Cart

User = get_user_model()


class CartSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления/удаления
    рецептов в корзину.
    """

    class Meta:
        model = Cart
        fields = ('user', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        recipe_id = data['recipe'].id
        cart_exists = Cart.objects.filter(
            user=request.user,
            recipe__id=recipe_id
        ).exists()

        if request.method == 'GET' and cart_exists:
            raise serializers.ValidationError(
                'Рецепт уже в списке покупок!'
            )

        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSubscriptionSerializer(
            instance.recipe,
            context=context).data
