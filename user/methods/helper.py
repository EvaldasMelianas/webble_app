from user.models import ReadingProgress, Review


def update_reading_progress(user, book_pk, current_page):
    if ReadingProgress.objects.filter(user=user, book=book_pk).exists():
        reading_progress = ReadingProgress.objects.get(pk=user, book=book_pk)
        if current_page > reading_progress.last_page_read:
            reading_progress.last_page_read = current_page
            reading_progress.save()
    else:
        reading_progress = ReadingProgress.objects.create(user_id=user, book=book_pk, last_page_read=current_page)
        reading_progress.save()


def get_review(user, book_pk):
    if Review.objects.filter(user=user, book=book_pk).exists():
        return Review.objects.get(user=user, book=book_pk)
