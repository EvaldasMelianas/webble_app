from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, CreateView, UpdateView, DeleteView

from user.models import ReadingProgress, Bookmark, Review
from webble.forms import RegistrationForm
from webble.models import Book


class RegisterView(FormView):
    """
    This view is responsible for obtaining and verifying the registration form.
    """
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


class UserDetails(DetailView):
    """
    This view is responsible for obtaining user relevant information.
    """
    model = User
    template_name = 'user_page.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        """
        Builds additional context with relevant user information.
        user_bookmark dictionary is build to access the needed bookmark information more conveniently.

        :param kwargs: retrieves context built by DetailView.
        :return: Context dictionary.
        """
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
        """
        This method handles the POST request for deleting bookmarks and progress.

        :param request: The HTTP POST request object.
        :param kwargs: Additional keyword arguments.
        :return: HTTP response.
        """
        if 'delete_bookmark' in request.POST:
            """
            Since 2 items are passed, we split them to obtain the title and page separately.
            We get the Bookmark object that matches the user, title and page. Then we delete.
            """
            title, page = request.POST['delete_bookmark'].split('|')
            bookmark = Bookmark.objects.get(
                user=self.request.user,
                book__title=title,
                page=page)
            bookmark.delete()
            messages.success(self.request, 'Bookmark deleted successfully')
        if 'delete_progress' in request.POST:
            """
            We filter by the request.user and primary key to obtain the specified entry. Then we delete.
            """
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

    def get_success_url(self):
        """
        On success, redirect to the book_detail page using the primary key of the book in the URL
        """
        return reverse_lazy('webble:book_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book = Book.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class UpdateReview(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ['rating', 'review']
    template_name = 'add_review.html'

    def get_success_url(self):
        """
        On success redirects to book_detail page.
        :return: The URL for the book_detail page with the primary key of the book in the URL.
        """
        return reverse_lazy('webble:book_detail', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, **kwargs):
        """
        Retrieves the submitted form for the review.pk and user pair.
        :return: Review object.
        """
        return Review.objects.get(user=self.request.user, pk=self.kwargs['review'])


class DeleteReview(LoginRequiredMixin, DeleteView):
    model = Review
    fields = ['rating', 'review']
    template_name = 'review_delete.html'

    def get_success_url(self):
        """
        On success redirects to book_detail page.
        :return: The URL for the book_detail page with the primary key of the book in the URL.
        """
        return reverse_lazy('webble:book_detail', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, **kwargs):
        """
        Retrieves the submitted form for the review.pk and user pair.
        :return: Review object.
        """
        return Review.objects.get(user=self.request.user, pk=self.kwargs['review'])
