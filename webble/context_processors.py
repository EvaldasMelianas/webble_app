from .models import Genre, Review


def get_genres(request):
    return {'genres': Genre.objects.all()}


def get_rating(request):
    return {'ratings': Review.objects.all()}
