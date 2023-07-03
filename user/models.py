from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.functions import Now

from webble.models import Book


class Bookmark(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    page = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['date']
        unique_together = ('book', 'user', 'page',)


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(max_length=150, null=True, blank=True)

    class Meta:
        ordering = ['date']
        unique_together = ('book', 'user',)


class ReadingProgress(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_started = models.DateField(default=Now)
    date_finished = models.DateField(null=True, blank=True)
    last_page_read = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.last_page_read == self.book.page_count:
            self.date_finished = Now
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('book', 'user', 'last_page_read')
