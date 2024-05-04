from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views import View

from .models import Profile

class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = "profile-update.html"


class Index(View):
    template_name = 'index.html'

    def get_context_data(self, *kwargs):
        ctx = 0
        return ctx