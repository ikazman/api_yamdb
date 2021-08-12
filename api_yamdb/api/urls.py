from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .views import (
    CommentViewSet, ReviewViewSet, UserViewSet
)

router = DefaultRouter()
router.register(
    r'v1/titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', 
    CommentViewSet,
    basename='comments'
)
router.register('v1/users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
