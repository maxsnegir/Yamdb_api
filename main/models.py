from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

from datetime import date

User = get_user_model()


class Title(models.Model):
    name = models.CharField('Название', max_length=255)
    year = models.PositiveIntegerField('Год создания', blank=True, null=True,
                                       validators=[MaxValueValidator(
                                           date.today().year)],
                                       db_index=True, )
    description = models.TextField('Описание', blank=True, null=True)
    genre = models.ManyToManyField('Genre', blank=True, verbose_name='Жанр', )
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 blank=True, null=True,
                                 verbose_name='Категория', )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Название категории', max_length=255)
    slug = models.SlugField('Слаг категории', unique=True, blank=True,
                            null=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=255)
    slug = models.SlugField('Слаг жанра', unique=True, blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Comment(models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE,
                               related_name='comments', db_index=True, )
    text = models.TextField('Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True,
                               verbose_name='Автор')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True,
                                    verbose_name='Дата публикации')

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Comment by {self.author}'


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews', db_index=True,
                              verbose_name='Произведения')
    text = models.TextField('Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews', db_index=True,
                               verbose_name='Автор')
    score = models.PositiveIntegerField('Оценка',
                                        validators=[MaxValueValidator(10), ])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True,
                                    db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_author'),
        ]
        ordering = ['pub_date']
        verbose_name_plural = 'Обзоры'
        verbose_name = 'Обзор'

    def __str__(self):
        return f"By {self.author} to {self.title}"
