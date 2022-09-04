from django.contrib import admin

from .models import (
    Recipe,
    Ingredient,
    Tag,
    Favorite,
    Cart,
    IngredientInRecipe
)


class RecipeIngredientInline(admin.TabularInline):
    model = IngredientInRecipe
    min_num = 1
    extra = 1


class RecipeTagInLine(admin.TabularInline):
    model = Recipe.tags.through
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'name',
        'image',
        'text',
        'favorites_count',
        'created',
    )
    search_fields = (
        'name',
        'author__username',
        'tags__name',
    )
    ordering = ('-created',)
    inlines = (RecipeIngredientInline, RecipeTagInLine,)
    readonly_fields = ('favorites_count', 'created')
    list_filter = (
        'name',
        'author',
        'tags',
        'created',
    )
    empty_value_display = '-пусто-'

    def favorites_count(self, obj):
        return obj.favorites_recipe.all().count()

    favorites_count.short_description = 'Добавлений в избранное'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = ('measurement_unit',)
    search_fields = ('name',)
    ordering = ('name',)
    empty_value_display = '-пусто-'


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ingredient',
        'recipe',
        'amount'
    )
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug'
    )
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
