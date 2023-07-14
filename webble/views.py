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


class HomeView(ListView):
    """
    This view is responsible for the landing page.
    """
    model = Genre
    context_object_name = 'genres'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        """
        Builds additional context needed.

        :param kwargs: retrieves context built by ListView.
        :return: Context dictionary
        """
        context = super().get_context_data(**kwargs)
        context['genre_books'] = get_books_by_genre(self.model, Book)
        return context


class AllAuthorsView(ListView):
    """
    This view is responsible for displaying all available authors.
    """
    model = Author
    template_name = 'all_authors.html'
    context_object_name = 'authors'
    ordering = 'name'
    paginate_by = 18


class AllBooksView(ListView):
    """
    This view is responsible for displaying all available books.
    """
    model = Book
    template_name = 'all_books.html'
    context_object_name = 'books'
    ordering = 'title'
    paginate_by = 18


class GenreListView(ListView):
    """
    This view is responsible for displaying books that fit the genre selected.
    """
    model = Genre
    template_name = 'genre_books.html'

    def get_context_data(self, **kwargs):
        """
        Builds additional context needed.
        Context['genre_books'] provides a list of book objects that can be displayed.
        Context['genre'] is the selected genre.

        :param kwargs: retrieves context built by ListView.
        :return: Context dictionary
        """
        context = super().get_context_data(**kwargs)
        genre = get_object_or_404(Genre, pk=self.kwargs['pk'])
        books = Paginator(Book.objects.filter(genres=genre).order_by('?'), 18)
        context['genre_books'] = books.get_page(self.request.GET.get('page'))
        context['genre'] = genre
        return context


class BookDetailView(DetailView):
    """
    This view is responsible for displaying information about a specified book.
    """
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        """
        Builds context needed to obtain needed information to display.
        Context[similar_books] provides random books that are similar to the book accessed.
        Context[reviews] provides all the reviews associated with the book.
        Context[rating] provides the average of all ratings for the associated book.

        :param kwargs: retrieves context built by DetailView.
        :return: Context dictionary
        """
        context = super().get_context_data(**kwargs)
        similar_books = Book.objects.filter(genres__in=self.object.genres.all()).exclude(pk=self.object.pk)
        context['similar_books'] = similar_books.order_by('?')[:5]
        context['reviews'] = Review.objects.filter(book__pk=self.object.pk)
        context['rating'] = context['reviews'].aggregate(Avg('rating'))['rating__avg']
        if self.request.user.is_authenticated:
            context['user_review'] = get_review(self.request.user, self.object.pk) or None
        return context


class AuthorDetailView(DetailView):
    """
    This view is responsible for displaying information about a specified author.
    """
    model = Author
    template_name = 'author_detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        """
        Handles building additional context with needed information.
        Obtain books written by the author object by filtering.

        :param kwargs: retrieves base context built by DetailView.
        :return: Context dictionary.
        """
        context = super().get_context_data(**kwargs)
        written_books = Book.objects.filter(authors=self.object)
        paginator = Paginator(written_books.order_by('?'), 6)
        context['written'] = paginator.get_page(self.request.GET.get('page'))
        return context


class SearchBookView(ListView):
    """
    This view is responsible for displaying the result of the searched phrase.
    """
    template_name = 'search_book.html'

    @staticmethod
    def post(request):
        """
        Handles the POST request for searching books and authors based on a given phrase.

        :param request: The incoming request object.
        :return: A rendered response with the search results.
        """
        searched = Book.objects.filter(title__icontains=request.POST.get('name'))
        searched_authors = Author.objects.filter(name__icontains=request.POST.get('name'))
        return render(request, 'search_book.html', {'searched_books': searched, 'searched_authors': searched_authors})


class ReadBookView(LoginRequiredMixin, DetailView):
    """
    This view is responsible for displaying and navigating through the selected book.
    """
    model = Book
    template_name = 'read_book.html'
    slug_field = 'title'
    slug_url_kwarg = 'title'

    def get_context_data(self, **kwargs):
        """
        Builds context needed to obtain needed information to display.

        :param kwargs: retrieves context built by DetailView and retrieves kwargs from URL.
        :return: Context dictionary
        """
        context = super().get_context_data(**kwargs)
        context['page_number'] = self.kwargs['page_number']
        context['next'], context['previous'] = self.kwargs['page_number']+1, self.kwargs['page_number']-1
        context['page_image'] = decode_image_data(get_pdf_data(self.object.pdf), context['page_number']-1)
        update_reading_progress(self.request.user, self.object, context['page_number'])
        return context

    def post(self, request, title: str, page_number: int):
        """
        Handles the POST request for creating a new bookmark.

        :param request: The incoming request object.
        :param title: The title of the book. Retrieved from the URL.
        :param page_number: The page number of the book. Retrieved from the URL.
        :return: A redirect response.
        """
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
