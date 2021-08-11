from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (CategoryViewSet, GenreViewSet,
                    TitleViewSet, UserViewSet, obtain_auth_token,
                    obtain_confirmation_code)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')

auth_urls = [
    path('email/', obtain_confirmation_code, name='confirmation_code_obtain'),
    path('token/', obtain_auth_token, name='token_obtain')
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router_v1.urls)),
]