from django.contrib import admin
from .models import Bookmark, Review, ReadingProgress

admin.site.register(Bookmark)
admin.site.register(Review)
admin.site.register(ReadingProgress)
