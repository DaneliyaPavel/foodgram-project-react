from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Recipe
from users.models import Subscription

User = get_user_model()


class SignUpSerializer(UserCreateSerializer):
    """
    Сериализатор для регистрации пользователей на сайте.
    """

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('email', 'username')
            )
        ]

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError("Имя me недопустимо!")
        return data


class CustomUserSerializer(UserSerializer):
    """
    Сериализатор для просмотра пользователя.
    """
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = (
            'id', 'username', 'email',
            'first_name', 'last_name',
            'is_subscribed'
        )
        read_only_fields = 'is_subscribed',

    def get_is_subscribed(self, obj):
        """
        Подписан ли текущий пользователь на
        просматриваемого.
        """
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj.id).exists()


class RecipeSubscriptionSerializer(serializers.ModelSerializer):
    """
    Cериализатор для рецепта в подписке.
    """
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('name', 'image', 'cooking_time')


class SubscriptionsListSerializer(serializers.ModelSerializer):
    """
    Мои подписки.
    Возвращает пользователей, на которых подписан текущий пользователь.
    В выдачу добавляются рецепты.
    """
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, author):
        if self.context['request'].user.is_anonymous:
            return False
        return Subscription.objects.filter(
            author=author, user=self.context['request'].user
        ).exists()

    @staticmethod
    def get_recipes_count(author):
        return author.user_recipe.all().count()

    def get_recipes(self, author):
        request = self.context['request']
        limit = request.GET.get('recipes_limit')
        author = get_object_or_404(User, id=author.pk)
        recipes = author.user_recipe.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeSubscriptionSerializer(
            recipes,
            many=True,
            context={'request': request}
        )
        return serializer.data
