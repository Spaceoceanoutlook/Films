from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Film(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")
    year = models.IntegerField(blank=True, verbose_name="Год выпуска")
    genre = models.ManyToManyField('Genre', verbose_name="Жанр", blank=True)
    country = models.ManyToManyField('Country', verbose_name="Страна", blank=True)
    rating = models.FloatField(blank=True, verbose_name="Рейтинг")
    content = models.TextField(blank=True, verbose_name="Описание")
    photo = models.ImageField(upload_to='films/static/films/img/', verbose_name="Постер", blank=True)
    recommendation = models.BooleanField(verbose_name="Рекомендовать", default=True)

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('film-info', kwargs={'film_pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class Comment(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Комментарий')
    published_date = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Genre(models.Model):
    title = models.CharField(max_length=100, blank=True, verbose_name='Жанр', default='Unknown')

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Country(models.Model):
    title = models.CharField(max_length=100, blank=True, verbose_name='Страна', default='Unknown')

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    films = models.ManyToManyField(Film, related_name='films')

    objects = models.Manager()

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
