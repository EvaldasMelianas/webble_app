from django.urls import path

from . import views

app_name = 'webble'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('authors/', views.AllAuthorsView.as_view(), name='all_authors'),
    path('books/', views.AllBooksView.as_view(), name='all_books'),
    path('category/<int:pk>/', views.GenreListView.as_view(), name='genre_detail'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('search/', views.SearchBookView.as_view(), name='search_book'),
    path('book/<str:title>/page/<int:page_number>/', views.ReadBookView.as_view(), name='read_book'),
]
