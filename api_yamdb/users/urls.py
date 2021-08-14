from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignupViewSet, TokenViewSet, UserViewSet

router_v1 = DefaultRouter()


router_v1.register(r'users', UserViewSet)

auth_patterns = [
    path('signup/', SignupViewSet.as_view({'post': 'signup'})),
    path('token/', TokenViewSet.as_view({'post': 'token'}), name='token'),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router_v1.urls)),
]
