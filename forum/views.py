from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Post, PostCategory


class ThreadListView(ListView):
    model = PostCategory
    template_name = "forum-list.html"


class ThreadDetailView(DetailView):
    model = Post
    template_name = "forum-detail.html"


class ThreadCreateView(CreateView):
    model = Post
    template_name = "forum-create.html"


class ThreadUpdateView(UpdateView):
    model = Post
    template_name = "forum-update.html"