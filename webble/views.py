from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

import random

from .models import Book, Author, Genre


class HomeView(View):

    def get(self, request):
        genres = Genre.objects.all()
        genre_books = {}
        for genre in genres:
            filtered_books = Book.objects.filter(genres=genre)
            genre_books[genre.genre] = filtered_books.order_by('?')[:6]
        return render(request, 'home.html', {'genre_books': genre_books})


class AllAuthorsView(ListView):
    model = Author
    template_name = 'all_authors.html'
    context_object_name = 'authors'
    ordering = 'name'
    paginate_by = 9


class AllBooksView(ListView):
    model = Book
    template_name = 'all_books.html'
    context_object_name = 'books'
    ordering = 'title'
    paginate_by = 9


class GenreListView(ListView):
    model = Genre
    template_name = 'genre_books.html'
    context_object_name = 'genre'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre_id = self.kwargs['pk']
        genre = get_object_or_404(Genre, pk=genre_id)
        context['genre_books'] = Book.objects.filter(genres=genre)
        context['genre'] = genre
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve similar books based on some common criteria
        similar_books = Book.objects.filter(genres__in=self.object.genres.all()).exclude(pk=self.object.pk)
        context['similar_books'] = similar_books.order_by('?')[:4]
        return context


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve books written by the author
        written_books = Book.objects.filter(authors=self.object)
        context['written'] = written_books.order_by('?')[:4]
        return context


class SearchBookView(View):
    paginate_by = 9

    def post(self, request):
        searched_books = Book.objects.filter(title__icontains=request.POST.get('name_of_book'))
        return render(request, 'search_book.html', {'searched_books': searched_books})


class ReadBookView(View):
    def get(self, request, book_pk, page_number):
        book = get_object_or_404(Book, pk=book_pk)
        # Open the PDF file and render the requested page
        doc = fitz.open(book.pdf.path)
        page = doc.load_page(page_number)
        pix = page.get_pixmap()
        image_data = pix.tobytes("png")
        # Pass the page details to the template
        return render(request, 'read_book.html', {'book': book, 'page': image_data, 'page_number': page_number})

    def post(self, request, book_pk, page_number):
        book = get_object_or_404(Book, pk=book_pk)
        if 'next' in request.POST:
            next_page_number = int(page_number) + 1
            # Navigate to the next page
            if 0 <= next_page_number < book.page_count:
                return redirect('read_book', book_pk=book_pk, page_number=next_page_number)
        elif 'previous' in request.POST:
            previous_page_number = int(page_number) - 1
            # Navigate to the previous page
            if 0 <= previous_page_number < book.page_count:
                return redirect('read_book', book_pk=book_pk, page_number=previous_page_number)
        elif 'bookmark' in request.POST:
            # Save the current page as a bookmark
            bookmark_page_number = int(page_number)
            bookmark = Bookmark.objects.create(book=book, user=request.user, page=bookmark_page_number)
            bookmark.save()
        else:
            return redirect('book_detail', pk=book_pk)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm(request)
    return render(request, 'registration/login.html', {'form': form})
