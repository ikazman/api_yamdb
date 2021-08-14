from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Comment, Review, User, Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'genre', 'category',)


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'genre', 'category',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.HyperlinkedRelatedField(
        view_name='review',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
<<<<<<< HEAD
        # exclude = ('review', )
=======
        exclude = ('review_id',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User
>>>>>>> user-app


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = Review
        fields = '__all__'
<<<<<<< HEAD
        exclude = ('title', )
=======
        exclude = ('title_id',)
>>>>>>> user-app
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title_id', 'author'),
                message="Возможен только один отзыв!"
            )
        ]
