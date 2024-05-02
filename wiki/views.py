from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Article, ArticleCategory
from .forms import ArticleForm, CommentForm
from user_management import models as ProfileModel


class ArticleListView(ListView):
	model = ArticleCategory
	template_name = "wiki-list.html"


class ArticleDetailView(DetailView):
	model = Article
	template_name = "wiki-detail.html"


class ArticleCreateView(CreateView):
	model = Article
	form_class = ArticleForm
	template_name = "wiki-create.html"


class ArticleUpdateView(UpdateView):
	model = Article
	form_class = ArticleForm
	template_name = "wiki-create.html"
