from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Thread, ThreadCategory
from .forms import ThreadForm, CommentForm


class ThreadListView(ListView):
    model = ThreadCategory
    template_name = "forum-list.html"


class ThreadDetailView(LoginRequiredMixin, DetailView):
    model = Thread
    form_class = CommentForm
    template_name = "forum-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_model = self.get_object()
        category = main_model.category
        threads_in_category = Thread.objects.filter(category=category)
        context['threads_in_category'] = threads_in_category
        return context


class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    form_class = ThreadForm
    template_name = "forum-create.html"

    def get_success_url(self):
        return reverse_lazy('forum:thread-detail', kwargs={
            'pk': self.object.pk
        })


class ThreadUpdateView(LoginRequiredMixin, UpdateView):
    model = Thread
    form_class = ThreadForm
    template_name = "forum-update.html"