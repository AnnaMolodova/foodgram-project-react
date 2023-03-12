from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import (CASCADE, CharField, EmailField, ForeignKey,
                              UniqueConstraint)


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    email = EmailField(
        max_length=254,
        unique=True,
        verbose_name='имейл'
    )
    username = CharField(
        max_length=150,
        verbose_name='логин'
    )
    first_name = CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = CharField(
        max_length=150,
        verbose_name='Фамилия'
    )

    class Meta:
        ordering = ('id', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Пользователь',
        related_name='follower',
    )
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Автор',
        related_name='following',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            UniqueConstraint(
                fields=('user', 'author',),
                name='unique_subscribe'
            ),
        )
