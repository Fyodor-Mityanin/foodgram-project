from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from . import views

token_router = [
    path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

v1_router = [
    path('subscriptions/', views.FollowCreate.as_view(), name='subscribe'),
    # path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]



urlpatterns = [
    path('v1/token/', include(token_router)),
    path('v1/', include(v1_router)),
]
