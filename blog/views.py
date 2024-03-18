from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from ledger.models import Article

class ArticleListView(ListView):
	model = Article  
	template_name = "article_list.html"

class ArticleDetailView(DetailView):
	model = Article
	template_name = "article.html"