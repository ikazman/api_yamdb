from django.shortcuts import get_object_or_404
from reviews.models import Review, User, Titles
from rest_framework import viewsets
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .permissions import OwnerOrReadOnly, Moderator


from .serializers import (CommentSerializer, ReviewSerializer, UserSerializer, CategorySerializer,
    GenreSerializer,
    TitleListSerializer,
    TitlePostSerializer)


#  на уровне проекта доступ есть только у админа,
#  но на уровне представлений права переопределяем на
#  возможность любому читать и собственнику - править.

class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListSerializer
        return TitlePostSerializer


class CategoryViewSet(ListModelMixin,
                      CreateModelMixin,
                      DestroyModelMixin,
                      GenericViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListModelMixin,
                   CreateModelMixin,
                   DestroyModelMixin,
                   GenericViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [OwnerOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get("title_id"))
        reviews = title.reviews.all()
        return reviews

    def perform_create(self, serializer):
        get_object_or_404(Titles, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user)

    def get_permissions(self, request):
        # Если человек модератор то может все менять
        if request.user == 'moderator':
            return (Moderator(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [OwnerOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        comments = review.comments.all()
        return comments

    def perform_create(self, serializer):
        get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user)

    def get_permissions(self, request):
        # Если человек модератор то может все менять
        if request.user == 'moderator':
            return (Moderator(),)
        # Для остальных ситуаций
        # оставим текущий перечень пермишенов без изменений
        return super().get_permissions()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [OwnerOrReadOnly]
