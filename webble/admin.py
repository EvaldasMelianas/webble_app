from django.contrib import admin
from .models import Book, Author, Genre, Bookmark, Review, ReadingProgress


admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Bookmark)
admin.site.register(Review)
admin.site.register(ReadingProgress)
