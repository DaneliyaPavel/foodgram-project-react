from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers

from api.serializers.users import RecipeSubscriptionSerializer
from recipes.models import Cart, Recipe

User = get_user_model()


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('user', 'recipe')

    def validate(self, data):
        if Cart.objects.filter(
                user=self.context['request'].user,
                recipe=data['recipe']
        ):
            raise serializers.ValidationError('Уже добавлен')
        return data

    def to_representation(self, instance):
        return RecipeSubscriptionSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data
