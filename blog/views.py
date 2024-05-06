from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ArticleForm, CommentForm
from .models import Article, ArticleCategory
from user_management import models as ProfileModel


class AuthorProfileMixin(object):
    def get_author_profile(self):
        if self.request.user.is_authenticated:
            author, _ = ProfileModel.Profile.objects.get_or_create(user=self.request.user)
            return author
        return None


class ArticleListView(AuthorProfileMixin, ListView):
    model = ArticleCategory
    template_name = "blog-list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        author = self.get_author_profile()
        if author:
            articles_by_author = Article.objects.filter(author=author)
            ctx['articles_by_author'] = articles_by_author
        return ctx


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog-detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        article = self.get_object()
        if self.request.user.is_authenticated:
            author = ProfileModel.Profile.objects.get(user=article.author.user) 
            articles_by_author = Article.objects.filter(author=author)
            ctx['articles_by_author'] = articles_by_author
            ctx['viewer'] = author
            ctx['form'] = CommentForm(initial={'author': author, 'article': article})
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        author = ProfileModel.Profile.objects.get(user=self.request.user)
        article = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = author
            comment.article = article
            comment.save()
            return redirect('blog:article-detail', pk=article.pk)
        ctx = self.get_context_data(**kwargs)
        return self.render_to_response(ctx)
    
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "blog-create.html"

    def get_success_url(self):
        return reverse_lazy('blog:article-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        author = ProfileModel.Profile.objects.get(user=self.request.user)
        form.instance.author = author
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        author = ProfileModel.Profile.objects.get(user=self.request.user)
        ctx['form'] = ArticleForm(initial={'author': author})
        return ctx
    
    def get_initial(self):
        author = ProfileModel.Profile.objects.get(user=self.request.user)
        return {'author':author}


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "blog-update.html"

    def get_success_url(self):
	    return reverse_lazy('blog:article-detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

