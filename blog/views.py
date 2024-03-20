# Create your views here.
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Article


class ArticleListView(ListView):
	model = Article  
	template_name = "article-list.html"

class ArticleDetailView(DetailView):
	model = Article
	template_name = "article-detail.html"