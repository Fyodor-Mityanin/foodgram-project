from django.urls import include, path
from .views import FollowCreate, FollowDelete


# v1_router = [
#     path('subscriptions/', views.FollowCreate.as_view(), name='subscribe'),
#     # path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]


urlpatterns = [
    path('v1/subscriptions/', FollowCreate.as_view(), name='subscribe'),
    path('v1/subscriptions/<int:author_id>/', FollowDelete.as_view(), name='subscribe'),
    # path('v1/', include(v1_router)),
]
