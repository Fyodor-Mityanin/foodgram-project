from django.urls import include, path
from .views import FollowCreate, FollowDelete, FavoriteCreate, FavoriteDelete, PurchaseCreate, PurchaseDelete, IngredientsSearch

urlpatterns = [
    path('v1/subscriptions/', FollowCreate.as_view(), name='add_subscribe'),
    path('v1/subscriptions/<int:author_id>/', FollowDelete.as_view(), name='remove_subscribe'),
    path('v1/favorites/', FavoriteCreate.as_view(), name='add_favorite'),
    path('v1/favorites/<int:recipe_id>/', FavoriteDelete.as_view(), name='remove_favorite'),
    path('v1/purchases/', PurchaseCreate.as_view(), name='add_purchase'),
    path('v1/purchases/<int:recipe_id>/', PurchaseDelete.as_view(), name='remove_favorite'),
    path('v1/ingredients', IngredientsSearch.as_view(), name='remove_favorite'),
    # path('v1/', include(v1_router)),
]
