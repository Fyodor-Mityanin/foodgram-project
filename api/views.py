from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView
from recipes.models import Favorite, Follow, User, Recipe
from .serializers import FollowSerializer, FavoriteSerializer
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

class FollowCreate(APIView):
    """Подписываемся на автора."""
    def post(self, request):
        author_id = request.data.get('id')
        author = get_object_or_404(User, id=author_id)
        # print(f'Автор - {author}')
        data = {
            'user': request.user.username, 
            'author': author.username, 
        }
        # print(f'Дата - {data}')
        serializer = FollowSerializer(data=data)
        if serializer.is_valid():
            # print(f'Сериализатор валидный')
            serializer.save()
            # print(f'Сериализатор сохранен')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowDelete(APIView):
    """Отписываемся от автора."""
    def get_object(self, author_id):
        # print('Заходим в гет_обжект')
        # print(author_id)
        author = get_object_or_404(User, id=author_id)
        # print('Получаем объект')
        # print(author_id)
        try:
            return Follow.objects.get(user=self.request.user, author=author)
        except Follow.DoesNotExist:
            raise Http404
    def delete(self, request, author_id, format=None):
        # print('Начало удаления')
        follow = self.get_object(author_id)
        follow.delete()
        return Response({'success': 'true'})   

class FavoriteCreate(APIView):
    """Добавляем в избранное."""
    def post(self, request):
        recipe_id = request.data.get('id')
        print(f'Рецепт - {recipe_id}')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        # print(f'Автор - {author}')
        data = {
            'user': request.user.username, 
            'recipe': recipe.slug, 
        }
        # print(f'Дата - {data}')
        serializer = FavoriteSerializer(data=data)
        if serializer.is_valid():
            # print(f'Сериализатор валидный')
            serializer.save()
            # print(f'Сериализатор сохранен')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavoriteDelete(APIView):
    """Удаляем из избранного."""
    def get_object(self, recipe_id):
        # print('Заходим в гет_обжект')
        # print(author_id)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        # print('Получаем объект')
        # print(author_id)
        try:
            return Favorite.objects.get(user=self.request.user, recipe=recipe)
        except Favorite.DoesNotExist:
            raise Http404
    def delete(self, request, recipe_id, format=None):
        # print('Начало удаления')
        favorite = self.get_object(recipe_id)
        favorite.delete()
        return Response({'success': 'true'})   

