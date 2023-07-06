from .models import Genre


# Obtain all Genres to iterate through them and display navbar choices in base.html.
def get_genres(request):
    return {
        'genres': Genre.objects.all()
    }
