from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from user.models import ReadingProgress, Review


# This function updates the readers progress once ReadBook view is accessed.
# We first check if the user already has progress on the book.
# If an entry is found we retrieve it and update according the defined logic.
# If no entry is found we create it.
def update_reading_progress(user, book, current_page):
    try:
        reading_progress = ReadingProgress.objects.get(user=user, book=book)
        if reading_progress.book.page_count >= current_page > reading_progress.last_page_read:
            if current_page == reading_progress.book.page_count:
                reading_progress.date_finished = timezone.now()
            reading_progress.last_page_read = current_page
            reading_progress.save()
    except ObjectDoesNotExist:
        reading_progress = ReadingProgress.objects.create(user=user, book=book, last_page_read=current_page)
        reading_progress.save()


# This function is used for BookDetail view, ascertain if the user reviewed the book.
# We filter the existing reviews via the user and book primary key.
# If an object is found, the user can edit his review instead of creating a new one.
# Logic handled in book_details.html
def get_review(user, book_pk):
    if Review.objects.filter(user=user, book=book_pk).exists():
        return Review.objects.get(user=user, book=book_pk)
