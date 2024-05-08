from django.shortcuts import render
from django.http import HttpResponse 
from django.views.generic.edit import UpdateView
from django.views import View

from .models import Profile
from merchstore import models as merchmodel
from forum import models as forummodel
from wiki import models as wikimodel
from blog import models as blogmodel
from commissions import models as commodel


class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = "profile-update.html"


class Index(View):
    template_name = 'index.html'

    def get_context_data(self, *kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['merchstore']
        return ctx
    
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