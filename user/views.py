from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, CreateView, UpdateView, DeleteView

from user.models import ReadingProgress, Bookmark, Review
from webble.forms import RegistrationForm
from webble.models import Book


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
                messages.error(self.request, error['message'])
        return super().form_invalid(form)


# User page view, displays bookmark and reading progress entries.
# The user_bookmark contact is a dict constructor that creates a key, value pair for title and the pages bookmarked.
# Context user_progress extracts all entries into the ReadingProgress model by the user.

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

    def post(self, request, **kwargs):
        # If delete_bookmark buttons is pressed, the title and page is passed to the POST request.
        # Since 2 items are passed, we split them to obtain the title and page separately.
        # We get the Bookmark object that matches the user, title and page. Then we delete.
        if 'delete_bookmark' in request.POST:
            title, page = request.POST['delete_bookmark'].split('|')
            bookmark = Bookmark.objects.get(
                user=self.request.user,
                book__title=title,
                page=page)
            bookmark.delete()
            messages.success(self.request, 'Bookmark deleted successfully')

        # If delete_progress is pressed, the primary key of the ReadingProgress entry is passed through POST.
        # We filter by the request.user and primary key to obtain the specified entry. Then we delete.
        if 'delete_progress' in request.POST:
            progress = ReadingProgress.objects.get(
                user=self.request.user,
                pk=request.POST['delete_progress'])
            progress.delete()
            messages.success(self.request, 'Progress deleted successfully')
        return self.get(request, **kwargs)


class CreateReview(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'review']
    template_name = 'add_review.html'

    # On success redirect to book_detail page using the primary key of the book in the URL.
    def get_success_url(self):
        return reverse_lazy('webble:book_detail', kwargs={'pk': self.kwargs['pk']})

    # The book object is found by passing the 'pk' argument in the URL.
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book = Book.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class UpdateReview(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ['rating', 'review']
    template_name = 'add_review.html'

    # On success redirect to book_detail page using the primary key of the book in the URL.
    def get_success_url(self):
        return reverse_lazy('webble:book_detail', kwargs={'pk': self.kwargs['pk']})

    # The specific review is found by checking for the primary key, that is passed through the URL part named 'review'.
    def get_object(self):
        return Review.objects.get(user=self.request.user, pk=self.kwargs['review'])


class DeleteReview(LoginRequiredMixin, DeleteView):
    model = Review
    fields = ['rating', 'review']
    template_name = 'review_delete.html'

    # On success redirect to book_detail page using the primary key of the book in the URL.
    def get_success_url(self):
        return reverse_lazy('webble:book_detail', kwargs={'pk': self.kwargs['pk']})

    # The specific review is found by checking for the primary key, that is passed through the URL part named 'review'.
    def get_object(self):
        return Review.objects.get(user=self.request.user, pk=self.kwargs['review'])
