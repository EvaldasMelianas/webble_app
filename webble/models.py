from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Avg
import fitz
import requests

from .methods.helper import get_image_data, get_summary


class Author(models.Model):
    name = models.CharField(max_length=60)
    bio = models.TextField(null=True, blank=True)
    portrait = models.ImageField(upload_to='author_portraits/', blank=True, null=True,)

    def save(self, *args, **kwargs):
        # Check if new entry is being created or updated
        if not self.pk:
            # Fetch wiki summary using helper function
            self.bio = get_summary(self.name)
            # Fetch the image data using helper function
            image_data = get_image_data(self.name)
            # Save image as portrait
            self.portrait.save(f'{self.name}.jpg', ContentFile(image_data), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    genre = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.genre}'


class Book(models.Model):
    title = models.CharField(max_length=60)
    authors = models.ManyToManyField(Author)
    genres = models.ManyToManyField(Genre)
    pdf = models.FileField(upload_to='books/')
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    publish_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    page_count = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Check if new entry is being created or updated
        if not self.pk:
            self.description = get_summary(self.title)
            # Open the uploaded PDF file and get the page count
            pdf_data = self.pdf.read()
            book = fitz.open(stream=pdf_data, filetype="pdf")
            self.page_count = book.page_count
            # Generate the cover image from the first page of the PDF
            pix = book.load_page(0).get_pixmap(alpha=False)
            image_data = pix.tobytes()
            # Save the cover image in the cover_image field
            self.cover_image.save(f'{self.title}.jpg', ContentFile(image_data), save=False)
        super().save(*args, **kwargs)

    def average_rating(self):
        # Get the average rating of the book, returns None if no reviews
        return self.object.reviews.aggregate(Avg('rating'))['rating__avg']

    def __str__(self):
        return f'{self.title}'


class Bookmark(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    page = models.IntegerField(null=True, blank=True)


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    rating = models.IntegerField(null=True, blank=True)
    review = models.TextField(max_length=150, null=True, blank=True)

    class Meta:
        ordering = ['date']
        unique_together = ('book', 'user',)


class ReadingProgress(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_started = models.DateField(auto_now_add=True)
    date_finished = models.DateField(null=True, blank=True)
    last_page_read = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('book', 'user',)
