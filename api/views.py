from django.http import JsonResponse
from rest_framework import mixins, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.response import Response

from recipes.models import Favorite, Follow, Ingredient, Purchase, Recipe, User

from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, PurchaseSerializer)

SUCCESS_RESPONSE = JsonResponse({'success': 'true'})
UNSUCCESS_RESPONSE = JsonResponse({'success': 'false'})


class CreateDestroyViewSet(viewsets.GenericViewSet,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin):
    pass


class CommonAPIViewSet(CreateDestroyViewSet):
    """Общий вьюсет для всех API"""

    queryset = None
    serializer_class = None
    get_obj_model = None
    get_obj_kwargs = None
    get_data_api_field = None
    get_data_model = None

    def get_data(self, request):
        id = request.data.get('id')
        obj = get_object_or_404(self.get_data_model, id=id)
        data = {
            'user': request.user.username,
            self.get_data_api_field: str(obj),
        }
        return data

    def get_kwargs_for_get_obj(self):
        id = self.kwargs.get('pk')
        return {'user': self.request.user, self.get_obj_kwargs: id}

    def get_obj(self):
        kwargs = self.get_kwargs_for_get_obj()
        return get_object_or_404(self.get_obj_model, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.get_data(request))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_obj()
        self.perform_destroy(instance)
        return SUCCESS_RESPONSE


class SubscriptionsViewSet(CommonAPIViewSet):
    """Добавление и удаление подписки"""

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    get_obj_model = Follow
    get_obj_kwargs = 'author__id'
    get_data_api_field = 'author'
    get_data_model = User


class FavoritesViewSet(CommonAPIViewSet):
    """Добавление и удаление лайка"""

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    get_obj_model = Favorite
    get_obj_kwargs = 'recipe__id'
    get_data_api_field = 'recipe'
    get_data_model = Recipe


class PurchasesViewSet(CommonAPIViewSet):
    """Добавление и удаление покупки"""

    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    get_obj_model = Purchase
    get_obj_kwargs = 'recipe__id'
    get_data_api_field = 'recipe'
    get_data_model = Recipe


class IngredientsSearch(ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']
