from django.contrib import admin
from .models import Bookmark, Review, ReadingProgress


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'user_username', 'date', 'page')
    search_fields = ('book__title', 'user__username', 'date')

    def book_title(self, obj):
        return obj.book.title
    book_title.short_description = 'Book Title'

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'User Username'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'user_username', 'date', 'rating', 'review')
    search_fields = ('book__title', 'user__username',)

    def book_title(self, obj):
        return obj.book.title
    book_title.short_description = 'Book Title'

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'User Username'


class ReadingProgressAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'user_username', 'date_started', 'date_finished', 'last_page_read')
    search_fields = ('book__title', 'user__username',)

    def book_title(self, obj):
        return obj.book.title
    book_title.short_description = 'Book Title'

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'User Username'


admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ReadingProgress, ReadingProgressAdmin)
