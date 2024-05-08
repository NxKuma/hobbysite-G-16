from django.shortcuts import render
from django.http import HttpResponse 
from django.views.generic.edit import UpdateView
from django.views import View
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from merchstore import models as merchmodel
from forum import models as forummodel
from wiki import models as wikimodel
from blog import models as blogmodel
from commissions import models as commodel


class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = "profile-update.html"


def registerPage(request):
    form = UserCreationForm
    if request == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

    ctx = {'form':form}
    return render(request, 'register.html', ctx)

    
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
