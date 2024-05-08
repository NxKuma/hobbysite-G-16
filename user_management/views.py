from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView


from .models import Profile
from .forms import RegisterForm

from merchstore import models as merchmodel
from forum import models as forummodel
from wiki import models as wikimodel
from blog import models as blogmodel
from commissions import models as commodel



class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['display_name', 'email']
    template_name = "profile-update.html"
    success_url = reverse_lazy("profile:index")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user_profile = form.save()
        user = user_profile.user
        user.email = form.cleaned_data.get('email')
        user.save()
        user_profile.save()
        return response


class RegisterProfileView(CreateView):
    model = Profile
    form_class = RegisterForm
    template_name = "register.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        reg_user = form.save()
        user_profile = Profile.objects.get(user=reg_user)
        user_profile.email = form.cleaned_data.get('email')
        user_profile.display_name = form.cleaned_data.get('display_name')
        user_profile.save()
        reg_user.save()
        login(self.request, reg_user, backend="django.contrib.auth.backends.ModelBackend")
        return response
    
    def get_success_url(self):
        return reverse_lazy('profile:index')
    
def index(request):
     ctx = {
         "models" :{
             "merchstore":merchmodel.ProductType,
             "forum":forummodel.ThreadCategory,
             "wiki":wikimodel.ArticleCategory,
             "commission":commodel.Commission,
             "blog":blogmodel.ArticleCategory,
         }
     }
     return render(request, 'index.html', ctx)
