from rest_framework import serializers

from reviews.models import Comment, Review, User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review_id = serializers.HyperlinkedRelatedField(view_name='review_id', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    title_id = serializers.SlugRelatedField(read_only=True, slug_field='title_id')

    class Meta:
        model = Review
        fields = '__all__'
