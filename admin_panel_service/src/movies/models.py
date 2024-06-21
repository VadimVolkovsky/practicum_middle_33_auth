import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    """Abstract base class for Time Stamp fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """Abstract base class for ID field."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    """Model for Genres."""
    name = models.CharField(_('name'), max_length=256)
    description = models.TextField(_('description'), blank=True, default='Oops, still no description')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class GenreFilmWork(UUIDMixin):
    """Model for Genre and Film relation."""
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = ("content\".\"genre_film_work")
        unique_together = ("film_work", "genre")


class Person(UUIDMixin, TimeStampedMixin):
    """ Model for Persons."""
    full_name = models.CharField(_('name'), max_length=256)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Actor')
        verbose_name_plural = _('Actors')


class PersonFilmWork(UUIDMixin):
    """Model for Person and Film relation."""
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = ("content\".\"person_film_work")
        unique_together = ("film_work", "person", "role")


class FilmWork(UUIDMixin, TimeStampedMixin):
    """ Model for Films."""
    class _FilmType(models.TextChoices):
        MOVIE = _('movie')
        TV_SHOW = _('tv_show')

    title = models.CharField(_('title'), max_length=256)
    description = models.TextField(_('description'), blank=True, default='Oops, still no description')
    creation_date = models.DateField(_('creation date'))
    file_path = models.TextField(_('file path'), blank=True, null=True)
    rating = models.FloatField(
        _('rating'),
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    type = models.CharField(_('type'), choices=_FilmType.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    persons = models.ManyToManyField(Person, through='PersonFilmWork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Film')
        verbose_name_plural = _('Films')
