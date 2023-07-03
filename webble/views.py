from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView

from user.models import Bookmark, Review
from .models import Book, Author, Genre
from .methods.helper import get_pdf_data, decode_image_data, get_books_by_genre
from user.methods.helper import get_review


class HomeView(ListView):
    model = Genre
    context_object_name = 'genres'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre_books'] = get_books_by_genre(self.model, Book)
        return context


class AllAuthorsView(ListView):
    model = Author
    template_name = 'all_authors.html'
    context_object_name = 'authors'
    ordering = 'name'
    paginate_by = 18


class AllBooksView(ListView):
    model = Book
    template_name = 'all_books.html'
    context_object_name = 'books'
    ordering = 'title'
    paginate_by = 18


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


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(book__pk=self.object.pk)
        similar_books = Book.objects.filter(genres__in=self.object.genres.all()).exclude(pk=self.object.pk)
        context['similar_books'] = similar_books.order_by('?')[:5]
        context['reviews'] = reviews
        if self.request.user.is_authenticated:
            context['user_review'] = get_review(self.request.user, self.object.pk) or None
        return context


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


class SearchBookView(ListView):
    model = Book
    template_name = 'search_book.html'
    paginate_by = 9

    def post(self, request):
        searched_books = Book.objects.filter(title__icontains=request.POST.get('name_of_book'))
        return render(request, 'search_book.html', {'searched_books': searched_books})


class ReadBookView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'read_book.html'
    slug_field = 'title'
    slug_url_kwarg = 'title'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_number'] = self.kwargs['page_number']-1
        context['next'], context['previous'] = self.kwargs['page_number']+1, self.kwargs['page_number']-1
        context['page_image'] = decode_image_data(get_pdf_data(self.object.pdf), context['page_number'])
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
