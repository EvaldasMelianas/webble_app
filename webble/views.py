from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView

from .forms import RegistrationForm
from .models import Book, Author, Genre, Bookmark, ReadingProgress, Review
from .methods.helper import convert_pdf_to_image, get_pdf_data, decode_image_data


class HomeView(ListView):
    model = Genre
    context_object_name = 'genres'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre_books = {}
        for genre in self.model.objects.all():
            filtered_books = Book.objects.filter(genres=genre)
            genre_books[genre.genre] = filtered_books.order_by('?')[:6]
        context['genre_books'] = genre_books
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

    def get_queryset(self):
        query = self.request.GET.get('name_of_book')
        return Book.objects.filter(title__icontains=query)


class ReadBookView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'read_book.html'
    slug_field = 'title'
    slug_url_kwarg = 'title'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookmark'] = Bookmark.objects.filter(user=self.request.user, book=self.object)
        context['page_number'] = self.kwargs['page_number']-1
        context['next'], context['previous'] = self.kwargs['page_number']+1, self.kwargs['page_number']-1
        pdf_data = get_pdf_data(self.object.pdf)
        image_data = convert_pdf_to_image(pdf_data, context['page_number'])
        context['page_image'] = decode_image_data(image_data)
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


class RegisterView(FormView):
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        for name, error_list in form.errors.get_json_data().items():
            for error in error_list:
                error_message = error['message']
                messages.error(self.request, error_message)
        return super().form_invalid(form)


class UserDetails(DetailView):
    model = User
    template_name = 'user_page.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_progress'] = ReadingProgress.objects.filter(user=self.object)
        user_bookmarks = {}
        for bookmark in Bookmark.objects.filter(user=self.object):
            title = bookmark.book.title
            page_number = bookmark.page
            if title not in user_bookmarks:
                user_bookmarks[title] = []
            user_bookmarks[title].append(page_number)
        context['user_bookmarks'] = user_bookmarks
        return context


class CreateReview(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'review']
    template_name = 'add_review.html'

    def get_success_url(self):
        book_pk = self.kwargs['pk']
        return reverse_lazy('webble:book_detail', kwargs={'pk': book_pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book = Book.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
