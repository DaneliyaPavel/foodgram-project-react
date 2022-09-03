from django.urls import include, path
from rest_framework import routers

from api.views.ingredients import IngredientViewSet
from api.views.recipes import RecipeViewSet
from api.views.tags import TagsViewSet
from api.views.users import (CustomUserViewSet, SubscribeViewSet,
                             SubscriptionsListView)

app_name = 'api'

router = routers.DefaultRouter()
router.register(
    r'users/subscriptions',
    SubscriptionsListView,
    basename='subscriptions'
)
router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        'users/<int:user_id>/subscribe/',
        SubscribeViewSet.as_view(),
        name='subscribe'
    ),

    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
