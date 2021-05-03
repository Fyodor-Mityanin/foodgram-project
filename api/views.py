from django.http import JsonResponse
from rest_framework import mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Favorite, Follow, Ingredient, Purchase, Recipe, User

from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, PurchaseSerializer)

SUCCESS_RESPONSE = {'success': 'true'}
API_BASENAMES = {
    'SubscriptionsAPI': (User, 'author',),
    'FavoritesAPI': (Recipe, 'recipe',),
    'PurchasesAPI': (Recipe, 'recipe',),
}


class CreateDestroyViewSet(viewsets.GenericViewSet,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin):
    pass


class CommonAPIViewSet(CreateDestroyViewSet):
    """Общий вьюсет для всех API"""

    queryset = None
    serializer_class = None

    def get_data(self, request):
        id = request.data.get('id')
        obj = get_object_or_404(API_BASENAMES[self.basename][0], id=id)
        data = {
            'user': request.user.username,
            API_BASENAMES[self.basename][1]: str(obj),
        }
        return data

    def get_obj(self):
        id = self.kwargs.get('pk')
        if self.basename == 'SubscriptionsAPI':
            return get_object_or_404(Follow, user=self.request.user, author__id=id)
        if self.basename == 'FavoritesAPI':
            return get_object_or_404(Favorite, user=self.request.user, recipe__id=id)
        if self.basename == 'PurchasesAPI':
            return get_object_or_404(Purchase, user=self.request.user, recipe__id=id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.get_data(request))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_obj()
        self.perform_destroy(instance)
        return JsonResponse(SUCCESS_RESPONSE)


class SubscriptionsViewSet(CommonAPIViewSet):
    """Добавление и удаление подписки"""

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class FavoritesViewSet(CommonAPIViewSet):
    """Добавление и удаление лайка"""

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class PurchasesViewSet(CommonAPIViewSet):
    """Добавление и удаление покупки"""

    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


class IngredientsSearch(APIView):
    """Находим список ингредиентов"""

    def get(self, request):
        ingredient_title = request.query_params['query'][:-1]
        ingredient_queryset = Ingredient.objects.filter(
            title__icontains=ingredient_title).all()
        ingredient_serializer = IngredientSerializer(
            ingredient_queryset, many=True)
        return Response(ingredient_serializer.data)
