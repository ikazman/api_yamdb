from django.shortcuts import get_object_or_404
from reviews.models import Review, User, Titles
from rest_framework import viewsets

from .permissions import OwnerOrReadOnly, Moderator


from .serializers import CommentSerializer, ReviewSerializer, UserSerializer


#  на уровне проекта доступ есть только у админа,
#  но на уровне представлений права переопределяем на
#  возможность любому читать и собственнику - править.


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
