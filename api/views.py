from django.http import Http404
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Favorite, Follow, Ingredient, Purchase, Recipe, User

from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, PurchaseSerializer)


class FollowCreate(APIView):
    """Подписываемся на автора."""

    def post(self, request):
        author_id = request.data.get('id')
        author = get_object_or_404(User, id=author_id)
        data = {
            'user': request.user.username,
            'author': author.username,
        }
        serializer = FollowSerializer(data=data)
        if serializer.is_valid() and data['user'] != data['author']:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowDelete(APIView):
    """Отписываемся от автора."""

    def get_object(self, author_id):
        author = get_object_or_404(User, id=author_id)
        try:
            return Follow.objects.get(user=self.request.user, author=author)
        except Follow.DoesNotExist:
            raise Http404

    def delete(self, request, author_id, format=None):
        follow = self.get_object(author_id)
        follow.delete()
        return Response({'success': 'true'})


class FavoriteCreate(APIView):
    """Добавляем в избранное."""

    def post(self, request):
        recipe_id = request.data.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        data = {
            'user': request.user.username,
            'recipe': recipe.slug,
        }
        serializer = FavoriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavoriteDelete(APIView):
    """Удаляем из избранного."""

    def get_object(self, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        try:
            return Favorite.objects.get(user=self.request.user, recipe=recipe)
        except Favorite.DoesNotExist:
            raise Http404

    def delete(self, request, recipe_id, format=None):
        favorite = self.get_object(recipe_id)
        favorite.delete()
        return Response({'success': 'true'})


class PurchaseCreate(APIView):
    """Добавляем в покупки."""

    def post(self, request):
        recipe_id = request.data.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        data = {
            'user': request.user.username,
            'recipe': recipe.slug,
        }
        serializer = PurchaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseDelete(APIView):
    """Удаляем из покупок."""

    def get_object(self, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        try:
            return Purchase.objects.get(user=self.request.user, recipe=recipe)
        except Purchase.DoesNotExist:
            raise Http404

    def delete(self, request, recipe_id, format=None):
        Purchase = self.get_object(recipe_id)
        Purchase.delete()
        return Response({'success': 'true'})


class IngredientsSearch(APIView):
    """Находим список ингредиентов"""

    def get(self, request):
        ingredient_title = request.query_params['query'][:-1]
        ingredient_queryset = Ingredient.objects.filter(
            title__startswith=ingredient_title).all()
        ingredient_serializer = IngredientSerializer(
            ingredient_queryset, many=True)
        return Response(ingredient_serializer.data)
