from django.contrib.admin import ModelAdmin, TabularInline, register
from recipes.models import (AmountIngredient, Favorite, Ingredient, Recipe,
                            ShoppingCart, Tag)


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('name', 'slug',)
    ordering = ('color', )
    empty_value_display = '-пусто-'


class AmountInrgedientInLine(TabularInline):
    model = AmountIngredient


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('^name', )
    list_filter = ('name', )
    inlines = (AmountInrgedientInLine, )
    empty_value_display = '-пусто-'


@register(AmountIngredient)
class AmountIngredientAdmin(ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount',)
    list_filter = ('ingredient', 'recipe', 'amount')
    empty_value_display = '-пусто-'


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('id', 'name', 'author', 'favorited')
    list_filter = ('name', 'author', 'tags',)
    search_fields = ('name', 'author', 'tags',)
    inlines = (AmountInrgedientInLine, )
    empty_value_display = '-пусто-'

    def favorited(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    favorited.short_description = 'В избранном'


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'
