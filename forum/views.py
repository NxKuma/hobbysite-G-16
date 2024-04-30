from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Thread, ThreadCategory
from .forms import ThreadForm


class ThreadListView(ListView):
    model = ThreadCategory
    template_name = "forum-list.html"


class ThreadDetailView(LoginRequiredMixin, DetailView):
    model = Thread
    template_name = "forum-detail.html"


class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    form_class = ThreadForm
    template_name = "forum-create.html"


class ThreadUpdateView(LoginRequiredMixin, UpdateView):
    model = Thread
    form_class = ThreadForm
    template_name = "forum-update.html"