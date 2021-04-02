from django.urls import include, path
from .views import FollowCreate, FollowDelete, FavoriteCreate, FavoriteDelete


# v1_router = [
#     path('subscriptions/', views.FollowCreate.as_view(), name='subscribe'),
#     # path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]


urlpatterns = [
    path('v1/subscriptions/', FollowCreate.as_view(), name='add_subscribe'),
    path('v1/subscriptions/<int:author_id>/', FollowDelete.as_view(), name='remove_subscribe'),
    path('v1/favorites/', FavoriteCreate.as_view(), name='add_favorite'),
    path('v1/favorites/<int:recipe_id>/', FavoriteDelete.as_view(), name='remove_favorite'),

    # path('v1/', include(v1_router)),
]
