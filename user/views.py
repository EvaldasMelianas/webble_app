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
        return reverse_lazy('webble:book_detail', kwargs={'pk': self.kwargs['pk']})

    def get_object(self):
        return Review.objects.get(pk=self.kwargs['review'])


class DeleteReview(LoginRequiredMixin, DeleteView):
    model = Review
    fields = ['rating', 'review']
    template_name = 'review_delete.html'

    def get_success_url(self):
        return reverse_lazy('webble:book_detail', kwargs={'pk': self.kwargs['pk']})

    def get_object(self):
        return Review.objects.get(pk=self.kwargs['review'])
