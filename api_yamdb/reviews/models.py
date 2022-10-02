from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        db_index=True
    )
    slug = models.SlugField(
        verbose_name='Обозначение',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return f'Категория "{self.name}"'


class Comment(models.Model):
    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        'User',
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    review = models.ForeignKey(
        'Review',
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)

    def __str__(self):
        return (f'Комментарий "{self.text[:settings.NUM_OF_DISP_SYMBOLS]}" '
                f'пользователя "{self.author.username}" '
                f'к отзыву "{self.review.text[:settings.NUM_OF_DISP_SYMBOLS]}"'
                f' пользователя "{self.review.author.username}" '
                f'на произведение "{self.review.title.name}" '
                f'из категории "{self.review.title.category.name}"'
                )


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        db_index=True
    )
    slug = models.SlugField(
        verbose_name='Обозначение',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return f'Жанр "{self.name}"'


class Review(models.Model):
    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        'User',
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(
                1,
                'Ваша оценка должна быть от 1 до 10 (целое число)'
            ),
            MaxValueValidator(
                10,
                'Ваша оценка должна быть от 1 до 10 (целое число)'
            )
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    title = models.ForeignKey(
        'Title',
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return (f'Отзыв "{self.text[:settings.NUM_OF_DISP_SYMBOLS]}" '
                f'пользователя "{self.author.username}" '
                f'на произведение "{self.title.name}" '
                f'из категории "{self.title.category.name}"'
                )


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        db_index=True
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year]
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return (f'Произведение "{self.name}" '
                f'из категории "{self.category.name}"')


class User(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'
    MODERATOR = 'moderator'
    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (USER, 'user'),
        (MODERATOR, 'moderator'),
    )
    email = models.EmailField(
        verbose_name='Эл. Почта',
        unique=True,
        max_length=254
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=ROLE_CHOICES,
        default=USER,
        max_length=9,
    )

    class Meta:
        ordering = ('role',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser or self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username
