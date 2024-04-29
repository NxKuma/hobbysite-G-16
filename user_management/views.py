from django.shortcuts import render
from django.views.generic.edit import UpdateView

from .models import Profile


class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = "profile-update.html"
