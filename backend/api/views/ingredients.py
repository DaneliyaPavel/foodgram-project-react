from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.filters import IngredientFilter
from api.serializers.ingredients import IngredientListSerializer
from recipes.models import Ingredient


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для работы с ингредиентами.
    Добавить тег может только пользователь.
    """
    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)
