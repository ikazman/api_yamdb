from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from datetime import datetime

User = get_user_model()

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Имя категории',
        help_text='Введите имя категории'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Ключевое слово',
        help_text='Введите ключевое слово',
        db_index=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ключевое слово'
        verbose_name_plural = 'Ключевые слова'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название',
        help_text='Введите название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Ключевое слово',
        help_text='Введите ключевое слово',
        db_index=True
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Произведение',
        help_text='Введите имя',
        max_length=100
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год',
        help_text='Введите год',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(datetime.now().year)
        ],
        db_index=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='title'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        null=True,
        related_name='title'
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
