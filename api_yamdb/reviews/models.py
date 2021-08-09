from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# ▼▼▼
class Title(models.Model):
    name = models.CharField(max_length=200)
    year = 
    category = models.ForeignKey('Category', related_name='comments')  

    def __str__(self):
        return self.name[:15]


# ▼▼▼
class Comment(models.Model):
    review_id = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')    
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text[:15]


# ▼▼▼
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


# ▼▼▼
class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )

    class Meta:
        constraints = (
            models.CheckConstraint(
                name='prevent_self_follow',
                check=~models.Q(user=models.F('following')),
            ),
            models.UniqueConstraint(fields=['user', 'following'],
                                    name='unique_followers')
        )

    def __str__(self):
        return f'follower: {self.user}, following: {self.following}'
