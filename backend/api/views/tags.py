from rest_framework.viewsets import ReadOnlyModelViewSet

from api.permissions import IsAdminOrReadOnly
from api.serializers.tags import TagListSerializer
from recipes.models import Tag


class TagsViewSet(ReadOnlyModelViewSet):
    """
    ViewSet для работы с тегами.
    Добавить тег может только администратор.
    """
    queryset = Tag.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    serializer_class = TagListSerializer
