from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Article, ArticleCategory


class ArticleListView(ListView):
	model = ArticleCategory
	template_name = "blog-list.html"


class ArticleDetailView(DetailView):
	model = Article
	template_name = "blog-detail.html"