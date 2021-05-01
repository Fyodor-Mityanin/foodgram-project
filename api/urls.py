from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

v1_router = DefaultRouter()

v1_router.register(
    'subscriptions',
    views.SubscriptionsViewSet,
    basename='SubscriptionsAPI',
)
v1_router.register(
    'favorites',
    views.FavoritesViewSet,
    basename='FavoritesAPI',
)
v1_router.register(
    'purchases',
    views.PurchasesViewSet,
    basename='PurchasesAPI',
)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/ingredients', views.IngredientsSearch.as_view(), name='remove_favorite'),
]
