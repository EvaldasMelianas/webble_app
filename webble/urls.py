from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from .views import *

app_name = 'webble'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('webble:home')), name='logout'),
    path('authors/', AllAuthorsView.as_view(), name='all_authors'),
    path('books/', AllBooksView.as_view(), name='all_books'),
    path('category/<int:pk>/', GenreListView.as_view(), name='genre_detail'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
    path('search/', SearchBookView.as_view(), name='search_book'),
    path('book/<int:book_pk>/page/<int:page_number>/', ReadBookView.as_view(), name='read_book'),
]
