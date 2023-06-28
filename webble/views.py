import base64

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views import View

from .forms import RegistrationForm
from .models import Book, Author, Genre, Bookmark
from .methods.helper import convert_pdf_to_image, get_pdf_data


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
    context_object_name = 'genre'
    paginate_by = 18

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
        context['similar_books'] = similar_books.order_by('?')[:5]
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


class ReadBookView(LoginRequiredMixin, View):
    def get(self, request, book_pk, page_number):
        book = get_object_or_404(Book, pk=book_pk)
        # Open the PDF file and render the requested page
        pdf_data = get_pdf_data(book.pdf)
        image_data = convert_pdf_to_image(pdf_data, page_number-1)
        image_data = base64.b64encode(image_data).decode('ascii')
        # Pass the page details to the template
        return render(request, 'read_book.html', {'book': book, 'page': image_data, 'page_number': page_number})

    def post(self, request, book_pk: int, page_number: int):
        book = get_object_or_404(Book, pk=book_pk)
        if 'next' in request.POST:
            page_number += 1
            return redirect('webble:read_book', book_pk=book_pk, page_number=page_number)
        elif 'previous' in request.POST:
            page_number -= 1
            return redirect('webble:read_book', book_pk=book_pk, page_number=page_number)

        elif 'bookmark' in request.POST:
            # Check if bookmark already exists for the page
            existing_bookmark = Bookmark.objects.filter(book=book, user=request.user, page=page_number)
            if existing_bookmark.exists():
                messages.warning(self.request, 'Bookmark already exists')
                return redirect('webble:read_book', book_pk=book_pk, page_number=page_number)

            else:
                # Save the current page as a bookmark
                bookmark = Bookmark.objects.create(book=book, user=request.user, page=page_number)
                bookmark.save()
                messages.success(self.request, 'Bookmark submission successful')
                return redirect('webble:read_book', book_pk=book_pk, page_number=page_number)
        else:
            return redirect('book_detail', pk=book_pk)


class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have been Signed Up!')
            return redirect('webble:home')
        return render(request, 'registration.html', {'form': form})
