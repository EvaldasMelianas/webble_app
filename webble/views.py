from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views import View

from .models import Book, Author, Genre


class HomeView(View):

    def get(self, request):
        genres = Genre.objects.all()
        genre_books = {}
        for genre in genres:
            filtered_books = Book.objects.filter(genres=genre)
            genre_books[genre.genre] = filtered_books
        return render(request, 'home.html', {'genre_books': genre_books})


class AllAuthorsView(ListView):
    model = Author
    template_name = 'all_authors.html'
    context_object_name = 'authors'
    ordering = 'name'


class AllBooksView(ListView):
    model = Book
    template_name = 'all_books.html'
    context_object_name = 'books'


class GenreDetailView(ListView):
    model = Genre
    template_name = 'genre_detail.html'
    context_object_name = 'genre'


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve similar books based on some common criteria
        similar_books = Book.objects.filter(genres__in=self.object.genres.all()).exclude(pk=self.object.pk)[:5]
        context['similar_books'] = similar_books
        return context


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve books written by the author
        written_books = Book.objects.filter(authors=self.object)
        context['written'] = written_books
        return context


class SearchBookView(View):

    def post(self, request):
        searched_books = Book.objects.filter(title__icontains=request.POST.get('name_of_book'))
        return render(request, 'search_book.html', {'searched_books': searched_books})


class ReadBookView(View):

  def get(self, request, book_pk, page_number):
    book = get_object_or_404(Book, pk=book_pk)
    page = convert_pdf_to_image(book.pdf, page_number)
    return render(request, 'read_book.html', {'page': page})
