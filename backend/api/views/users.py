from django.contrib.auth import get_user_model
from django.db import transaction
from djoser.views import UserViewSet
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers.users import (
    CustomUserSerializer,
    SubscriptionsListSerializer,
)
from core.pagination import CustomPageNumberPagination
from users.models import Subscription

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """
    ViewSet для работы с пользователями.
    """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_backends = (
        filters.SearchFilter,
    )
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = CustomUserSerializer(user, many=False)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return request


class SubscriptionsListView(ReadOnlyModelViewSet):
    """
    ViewSet для вывода списка подписок пользователя.
    """
    queryset = User.objects.all()
    serializer_class = SubscriptionsListSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    permission_classes = [IsAuthenticated]
    search_fields = ('^following__user',)

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(
            following__user=user
        )


class SubscribeViewSet(APIView):
    """
    APIView для подписки и отписки на/от автора
    """
    serializer_class = SubscriptionsListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        if user_id == request.user.id:
            return Response(
                {'error': 'Нельзя подписаться на себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Subscription.objects.filter(
                user=request.user,
                author_id=user_id
        ).exists():
            return Response(
                {'error': 'Вы уже подписаны на пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author = get_object_or_404(User, id=user_id)
        Subscription.objects.create(
            user=request.user,
            author_id=user_id
        )
        return Response(
            self.serializer_class(author, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        get_object_or_404(User, id=user_id)
        subscription = Subscription.objects.filter(
            user=request.user,
            author_id=user_id
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Вы не подписаны на пользователя'},
            status=status.HTTP_400_BAD_REQUEST
        )
