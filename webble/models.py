from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Avg

from .methods.helper import get_image_data, get_summary, convert_pdf_to_image, get_pdf_data


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
            if image_data is None:
                self.portrait = 'author_portraits/not_found.jpg'
            else:
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
    cover_image = models.ImageField(upload_to='covers/', blank=True)
    publish_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    page_count = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Check if new entry is being created or updated
        if not self.pk:
            self.description = get_summary(self.title)
            # Open the uploaded PDF file and get the page count
            pdf_data = get_pdf_data(self.pdf)
            self.page_count = pdf_data.page_count
            # Generate the cover image from the first page of the PDF
            image_data = convert_pdf_to_image(pdf_data, 0)
            # Assign the cover image in the cover_image field
            self.cover_image.save(f'{self.title}.jpg', ContentFile(image_data), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'
