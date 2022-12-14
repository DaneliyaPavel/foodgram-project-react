from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
