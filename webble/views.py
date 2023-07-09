from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView

from user.models import Bookmark, Review
from .models import Book, Author, Genre
from .methods.helper import get_pdf_data, decode_image_data, get_books_by_genre
from user.methods.helper import get_review, update_reading_progress


# Landing page view, displays 4 random genres and 6 books associated with them.
# Logic behind the sorting of genres and books is within get_books_by_genre.
class HomeView(ListView):
    model = Genre
    context_object_name = 'genres'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre_books'] = get_books_by_genre(self.model, Book)
        return context


# Author page view, displays 18 authors per page.
class AllAuthorsView(ListView):
    model = Author
    template_name = 'all_authors.html'
    context_object_name = 'authors'
    ordering = 'name'
    paginate_by = 18


# Book page view, displays 18 books per page.
class AllBooksView(ListView):
    model = Book
    template_name = 'all_books.html'
    context_object_name = 'books'
    ordering = 'title'
    paginate_by = 18


# Book sort view by genres, enables dropdown choice URLs in base.html
class GenreListView(ListView):
    model = Genre
    template_name = 'genre_books.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = get_object_or_404(Genre, pk=self.kwargs['pk'])
        paginator = Paginator(Book.objects.filter(genres=genre).order_by('?'), 18)
        context['genre_books'] = paginator.get_page(self.request.GET.get('page'))
        context['genre'] = genre
        return context


# View to display details for the accessed book.
# Context similar books builds list of books with matching genres.
# Context reviews retrieves the reviews that are associated with the book object.
# Context rating retrieves the ratings from reviews and calculates an average.
# If statement checks the user has already created a review, used for HTML to direct user to create or edit review.
class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        similar_books = Book.objects.filter(genres__in=self.object.genres.all()).exclude(pk=self.object.pk)
        context['similar_books'] = similar_books.order_by('?')[:5]
        context['reviews'] = Review.objects.filter(book__pk=self.object.pk)
        context['rating'] = context['reviews'].aggregate(Avg('rating'))['rating__avg']
        if self.request.user.is_authenticated:
            context['user_review'] = get_review(self.request.user, self.object.pk) or None
        return context


# Displays details associated with Author object.
# Context written extracts list of books that were written by the same author.
class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        written_books = Book.objects.filter(authors=self.object)
        paginator = Paginator(written_books.order_by('?'), 6)
        context['written'] = paginator.get_page(self.request.GET.get('page'))
        return context


# Enables the search option in base.html, to search books by title or author name.
# Filters book by the search title or Author.
class SearchBookView(ListView):
    template_name = 'search_book.html'

    def post(self, request):
        searched = Book.objects.filter(title__icontains=request.POST.get('name'))
        searched_authors = Author.objects.filter(name__icontains=request.POST.get('name'))
        return render(request, 'search_book.html', {'searched_books': searched, 'searched_authors': searched_authors})


# View for reading a single page of a selected book.
# Book object retrieve by using the slug_field.
# Context builds page_numer, next(page), previous(page) from the page_number argument in the URL.
# page_image utilizes helper methods to retrieve and encode the data for the HTML template to display.
# update_reading_progress checks and updates the current user progress for the book.
class ReadBookView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'read_book.html'
    slug_field = 'title'
    slug_url_kwarg = 'title'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_number'] = self.kwargs['page_number']
        context['next'], context['previous'] = self.kwargs['page_number']+1, self.kwargs['page_number']-1
        context['page_image'] = decode_image_data(get_pdf_data(self.object.pdf), context['page_number']-1)
        update_reading_progress(self.request.user, self.object, context['page_number'])
        return context

    def post(self, request, title: str, page_number: int):
        book = get_object_or_404(Book, title=title)
        if 'bookmark' in request.POST:
            existing_bookmark = Bookmark.objects.filter(book=book, user=request.user, page=page_number)
            if existing_bookmark.exists():
                messages.warning(self.request, 'Bookmark already exists')
            else:
                bookmark = Bookmark.objects.create(book=book, user=request.user, page=page_number)
                bookmark.save()
                messages.success(self.request, 'Bookmark submission successful')
            return redirect('webble:read_book', title=book.title, page_number=page_number)
