from datetime import datetime

from django.core.validators import MaxValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название',
        help_text='Введите название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Тег',
        help_text='Введите тег',
        db_index=True
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Жанр',
        help_text='Введите Жанр'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Тег',
        help_text='Введите тег',
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
        verbose_name='Название',
        help_text='Введите название',
        max_length=100
    )    
    year = models.PositiveSmallIntegerField(
        verbose_name='Год',
        help_text='Введите год',
        validators=[MaxValueValidator(datetime.today().year)],
        db_index=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )
    genre = models.ManyToManyField(Genre)

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
