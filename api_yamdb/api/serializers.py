from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Comment, Review, User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review_id = serializers.HyperlinkedRelatedField(
        view_name='review_id',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
        exclude = ('review_id', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title_id = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title_id'
    )

    class Meta:
        model = Review
        fields = '__all__'
        exclude = ('title_id', )
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title_id', 'author'),
                message="Возможен только один отзыв!"
            )
        ]
