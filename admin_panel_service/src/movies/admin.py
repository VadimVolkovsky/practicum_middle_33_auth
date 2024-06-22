from django.contrib import admin
from .models import Genre, FilmWork, GenreFilmWork, Person, PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at',)
    search_fields = ('name',)


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created_at', 'updated_at',)
    search_fields = ('full_name',)


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)
    list_display = (
        'title', 'type', 'creation_date', 'rating', 'created_at', 'updated_at'
    )
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id',)
