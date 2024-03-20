from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post, PostCategory


class ThreadListView(ListView):
    model = PostCategory
    template_name = "forum-list.html"


class ThreadDetailView(DetailView):
    model = Post
    template_name = "forum-detail.html"