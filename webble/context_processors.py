from .models import Genre


def get_items(request):
    return {'genres': Genre.objects.all()}
