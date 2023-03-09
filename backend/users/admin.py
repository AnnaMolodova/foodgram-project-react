from django.contrib.admin import ModelAdmin, register

from .models import Subscribe, User


@register(User)
class UserAdmin(ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'password'
    )
    list_filter = ('email', 'username')
    search_fields = ('username', 'email', )
    empty_value_display = '-пусто-'


@register(Subscribe)
class SubscribeAdmin(ModelAdmin):
    list_display = (
        'id',
        'user',
        'author'
    )
    search_fields = ('user', )
    list_filter = ('user', )
    empty_value_display = '-пусто-'
