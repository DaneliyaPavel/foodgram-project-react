from rest_framework import serializers

from recipes.models import Tag


class TagListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с тегами.
    """
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']
        read_only_fields = ['name', 'color', 'slug']
