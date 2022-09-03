from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import Q, F


class User(AbstractUser):
    """
    Модель пользователя.
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        help_text=(
            'Обязательное поле. До 150 символов. Буквы, цифры разрешены.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует'
        },
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=False,
        help_text='Укажите своё имя',
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=False,
        help_text='Укажите свою фамилию',
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
        blank=False,
        error_messages={
            'unique': 'Пользователь с таким email уже существует!',
        },
        help_text='Укажите свой email',
    )
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['last_name']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Subscription(models.Model):
    """
    Модель для подписок пользователей на автора рецепта.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow',
            ),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='self_following',
            ),
        )

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
