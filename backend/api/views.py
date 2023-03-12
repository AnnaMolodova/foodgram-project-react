from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (AmountIngredient, Favorite, Ingredient, Recipe,
                            ShoppingCart, Tag)
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import Subscribe, User

from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAuthorAdminOrReadOnly
from .serializers import (BaseUserSerializer, FavoriteSerializer,
                          IngredientSerializer, PasswordSerializer,
                          RecipeCreateSerializer, RecipeListSerializer,
                          ShoppingCartSerializer, SubscribeSerializer,
                          TagSerializer)


class ListRetrieveViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class SubscribePasswordUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = BaseUserSerializer

    @action(methods=['POST'],
            detail=False,
            permission_classes=(IsAuthenticated,))
    def set_password(self, request, pk=None):
        user = self.request.user
        serialier = PasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serialier.is_valid(raise_exception=True)
        user.set_password(serialier.validated_data['new_password'])
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'],
            detail=False,
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST', 'DELETE'],
            detail=True,
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id):
        user = self.request.user
        author = get_object_or_404(User, id=id)
        subscribe = Subscribe.objects.filter(user=user, author=author)
        if request.method == 'POST':
            if subscribe.exists():
                data = {
                    'errors': 'Нельзя подписаться на самого себя'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            Subscribe.objects.create(user=user, author=author)
            serializer = SubscribeSerializer(
                author,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not subscribe.exists():
                data = {'errors': 'Вы не подписаны на пользователя'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    permission_classes = (IsAuthorAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = PageNumberPagination

    def get_list(self, request, list_model, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        in_list = list_model.objects.filter(user=user, recipe=recipe)
        if request.method == 'POST':
            if not in_list:
                list_objects = list_model.objects.create(user=user,
                                                         recipe=recipe)
                if isinstance(list_model, Favorite):
                    serializer = FavoriteSerializer(list_objects.recipe)
                else:
                    serializer = ShoppingCartSerializer(
                        list_objects.recipe
                    )
                return Response(data=serializer.data,
                                status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not in_list:
                data = {
                    'errors': 'Рецепта нет в списке'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            in_list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['POST', 'DELETE'],
            detail=True,
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk=None):
        return self.get_list(request=request, list_model=Favorite, pk=pk)

    @action(methods=['POST', 'DELETE'],
            detail=True,
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        return self.get_list(request=request, list_model=ShoppingCart, pk=pk)

    @action(methods=['GET'],
            detail=False,
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = AmountIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values_list(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by().annotate(
            Sum('amount')
        )
        shopping_list = 'Список покупок: \n'
        for ingredient in ingredients:
            name, measure, amount = ingredient
            shopping_list += f'{name}'
            shopping_list += f'({measure})'
            shopping_list += f' — {amount}\n'
        response = HttpResponse(shopping_list, 'Content-Type: application/txt')
        response['Content-Disposition'] = (
            'attachment;'
            'filename="shoppinglist.txt"'
        )
        return response
