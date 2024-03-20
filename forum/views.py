from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post


class ThreadListView(ListView):
    model = Post
    template_name = "forum-list.html"


class ThreadDetailView(DetailView):
    model = Post
    template_name = "forum-detail.html"