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

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			author = ProfileModel.Profile.objects.get(user=self.request.user)
			articles_by_author = Article.objects.filter(author=author)
			ctx['articles_by_author'] = articles_by_author
		return ctx


class ArticleDetailView(DetailView):
	model = Article
	template_name = "wiki-detail.html"

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		if self.object:
			article = self.get_object()
			articles_by_author = Article.objects.filter(article_category=article.article_category)
			ctx['articles_by_author'] = articles_by_author
			if self.request.user.is_authenticated:
				author = ProfileModel.Profile.objects.get(user=self.request.user)
				ctx['viewer'] = author
				ctx['form'] = CommentForm(
				initial={
                        'author':author, 
                        'article':Article.objects.get(pk=article.pk)
                    }
                )
		return ctx

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		author = ProfileModel.Profile.objects.get(user=self.request.user)
		article  = self.get_object()
		form = CommentForm(request.POST,initial={
                    'author':author, 
                    'article':Article.objects.get(pk=article.pk)
                }
            )
		if form.is_valid():
			comment = form.save(commit=False)
			comment.author = author
			comment.post = article
			comment.save()
			return redirect('wiki:article-detail', pk=self.object.pk)
		ctx = self.get_context_data(**kwargs)
		return self.render_to_response(ctx)
        
    
	def form_valid(self, form):
		author = ProfileModel.Profile.objects.get(user=self.request.user)
		form.instance.author = author
		return super().form_valid(form)


class ArticleCreateView(LoginRequiredMixin, CreateView):
	model = Article
	form_class = ArticleForm
	template_name = "wiki-create.html"

	def get_success_url(self):
		return reverse_lazy('wiki:article-detail', kwargs={
            'pk': self.object.pk
        })
    
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)
    
	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		author = ProfileModel.Profile.objects.get(user=self.request.user)
		ctx['form'] = ArticleForm(
            initial={
                'author':author,
            }
        )
		return ctx


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
	model = Article
	form_class = ArticleForm
	template_name = "wiki-update.html"

	def get_success_url(self):
		return reverse_lazy('wiki:article-detail', kwargs={
            'pk': self.object.pk
        })
    
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)
