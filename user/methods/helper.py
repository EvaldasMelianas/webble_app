from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from user.models import ReadingProgress, Review


def update_reading_progress(user, book, current_page):
    """
    This function updates the reader's progress once the ReadBook view is accessed.

    :param user: User object
    :param book: Book object
    :param current_page: Current page number
    """
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


def get_review(user, book_pk):
    """
    This function is used for the BookDetail view to ascertain if the user has reviewed the book.
    If an object is found, the user can edit their review instead of creating a new one.

    :param user: User object
    :param book_pk: Book primary key
    :return: Review object if found, else None
    """
    if Review.objects.filter(user=user, book=book_pk).exists():
        return Review.objects.get(user=user, book=book_pk)
