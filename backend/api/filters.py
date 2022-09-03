from django.contrib.auth import get_user_model
from django_filters import FilterSet, filters

from recipes.models import Ingredient, Recipe

User = get_user_model()


class IngredientFilter(FilterSet):
    """
    Фильтр поиска ингредиентов по имени.
    """
    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    """
    Фильтр для сортировки рецептов по
    тегам, нахождению в избранном и корзине.
    """
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorites_recipe__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(cart_recipe__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')
