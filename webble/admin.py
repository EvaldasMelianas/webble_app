from django.contrib import admin
from .models import Book, Author, Genre


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'display_authors', 'display_genres', 'publish_date')
    search_fields = ('title', 'authors__name',)

    def display_authors(self, obj):
        return ', '.join([author.name for author in obj.authors.all()])
    display_authors.short_description = 'Authors'

    def display_genres(self, obj):
        return ', '.join([genre.genre for genre in obj.genres.all()])
    display_genres.short_description = 'Genres'


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')
    search_fields = ('name',)


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
