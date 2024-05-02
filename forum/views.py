from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Thread, ThreadCategory
from .forms import ThreadForm, CommentForm
from user_management import models as ProfileModel


class ThreadListView(ListView):
    model = ThreadCategory
    template_name = "forum-list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            author = ProfileModel.Profile.objects.get(user=self.request.user)
            threads_by_author = Thread.objects.filter(author=author)
            ctx['threads_by_author'] = threads_by_author
        return ctx


class ThreadDetailView(LoginRequiredMixin, DetailView):
    model = Thread
    template_name = "forum-detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.object:
            author = ProfileModel.Profile.objects.get(user=self.request.user)
            thread = self.get_object()
            threads_in_category = Thread.objects.filter(category=thread.category)
            ctx['threads_in_category'] = threads_in_category
            ctx['viewer'] = author
            ctx['form'] = CommentForm(
                initial={
                    'author':author, 
                    'thread':Thread.objects.get(pk=thread.pk)
                }
            )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        author = ProfileModel.Profile.objects.get(user=self.request.user)
        thread = self.get_object()  # Get object if needed for context
        form = CommentForm(request.POST,initial={
                    'author':author, 
                    'thread':Thread.objects.get(pk=thread.pk)
                }
            )
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = author
            comment.post = thread
            comment.save()
            return redirect('forum:thread-detail', pk=self.object.pk)
        ctx = self.get_context_data(**kwargs)
        return self.render_to_response(ctx)
        
    
    def form_valid(self, form):
        author = ProfileModel.Profile.objects.get(user=self.request.user)
        form.instance.author = author
        return super().form_valid(form)


class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    form_class = ThreadForm
    template_name = "forum-create.html"

    
    def get_success_url(self):
        return reverse_lazy('forum:thread-detail', kwargs={
            'pk': self.object.pk
        })
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        author = ProfileModel.Profile.objects.get(user=self.request.user)
        ctx['form'] = ThreadForm(
            initial={
                'author':author,
            }
        )
        return ctx


class ThreadUpdateView(LoginRequiredMixin, UpdateView):
    model = Thread
    form_class = ThreadForm
    template_name = "forum-update.html"

    def get_success_url(self):
        return reverse_lazy('forum:thread-detail', kwargs={
            'pk': self.object.pk
        })
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)