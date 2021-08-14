from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .views import (
    CommentViewSet, ReviewViewSet, UserViewSet, GenreViewSet, TitleViewSet
)

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
