from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import (CASCADE, CharField, DateTimeField, ForeignKey,
                              ImageField, ManyToManyField,
                              PositiveSmallIntegerField, SlugField, TextField,
                              UniqueConstraint)

User = get_user_model()


class Tag(models.Model):
    name = CharField(
        verbose_name='Тэг',
        max_length=200,
        unique=True,
    )
    color = CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
        db_index=False,
    )
    slug = SlugField(
        verbose_name='Слаг tag',
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    name = CharField(
        verbose_name='Ингредиент',
        max_length=200,
    )
    measurement_unit = CharField(
        verbose_name='Единица измерения',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    ingredients = ManyToManyField(
        verbose_name='Ингредиенты',
        related_name='recipe',
        to=Ingredient,
        through='AmountIngredient',
    )
    tags = ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipe',
    )
    image = ImageField(
        verbose_name='Катринка',
        upload_to='recipes/image/',
    )
    name = CharField(
        verbose_name='Название блюда',
        max_length=200,
    )
    text = TextField(
        verbose_name='Описание блюда',
    )
    cooking_time = PositiveSmallIntegerField(
        validators=[MinValueValidator(
            1, message='Слишком маленькое время приготовления'),
            MaxValueValidator(
            1000, message='Слишком долго'
        ), ],
        verbose_name='Время приготовления в минутах',
    )
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        null=True,
        verbose_name='Автор',
        related_name='recipes',
    )
    pub_date = DateTimeField(
        verbose_name='Дата',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )

    def __str__(self):
        return f'{self.name} {self.author.username}'


class AmountIngredient(models.Model):
    recipe = ForeignKey(
        to=Recipe,
        on_delete=CASCADE,
        verbose_name='Рецепт',
        related_name='amount_ingredient'
    )
    ingredient = ForeignKey(
        to=Ingredient,
        on_delete=CASCADE,
        verbose_name='Ингредиент',
        related_name='amount_ingredient'
    )
    amount = PositiveSmallIntegerField(
        validators=[MinValueValidator(
            1, message='Нужно хоть немного'),
            MaxValueValidator(
            50, message='Слишком долго'
        ), ],
        verbose_name='Количество',
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=('recipe', 'ingredient'),
                             name='unique_ingredient_recipe')
        ]
        ordering = ('id',)
        verbose_name = 'Кол-во ингредиента'
        verbose_name_plural = 'Количество ингредиента'

    def __str__(self):
        return f'{self.amount} {self.ingredient}'


class Favorite(models.Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Пользователь',
        related_name='favorites',
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='Любимый Рецепт',
        related_name='favorites',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(models.Model):
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='Рецепт',
        related_name='shopping_cart'
    )
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Пользователь',
        related_name='shopping_cart'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_cart'
            )
        ]
        ordering = ('id',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.recipe} в списке у {self.user}'
