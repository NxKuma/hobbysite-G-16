from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post, PostCategory

class ThreadListView(ListView):
    model = PostCategory