from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers.cart import CartSerializer
from api.serializers.favorite import FavoriteSerializer
from api.serializers.recipes import (
    RecipeListSerializer, RecipeCreateSerializer)
from core.pagination import CustomPageNumberPagination
from core.pdf_generator import pdf_shopping_list_generator
from recipes.models import Recipe, Favorite, Cart


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для обработки запросов к рецептам.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return RecipeCreateSerializer
        if self.request.method == 'GET':
            return RecipeListSerializer
        return self

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @staticmethod
    def post(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self.post(
            request=request, pk=pk, serializers=FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete(
            request=request, pk=pk, model=Favorite)

    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.post(
            request=request, pk=pk, serializers=CartSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete(
            request=request, pk=pk, model=Cart)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        return pdf_shopping_list_generator(user)
