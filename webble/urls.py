from django.urls import path

from .views import *

app_name = 'webble'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('authors/', AllAuthorsView.as_view(), name='all_authors'),
    path('books/', AllBooksView.as_view(), name='all_books'),
    path('category/<int:pk>/', GenreDetailView.as_view(), name='category_detail'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
    path('search/', SearchBookView.as_view(), name='search_book'),
    path('book/<int:book_pk>/page/<int:page_number>/', ReadBookView.as_view(), name='page_view'),
]
