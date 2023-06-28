from .models import Genre, Review


def get_items(request):
    return {'genres': Genre.objects.all(), 'reviews': Review.objects.all()}
