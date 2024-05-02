from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Product, ProductType, Transaction
from .forms import ProductForm, TransactionForm

from user_management import models as ProfileModel

class ProductListView(ListView):
    model = ProductType
    template_name = 'merchstore-list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            owner = ProfileModel.Profile.objects.get(user=self.request.user)
            products_by_owner = Product.objects.filter(owner=owner)
            ctx['products_by_owner'] = products_by_owner
        return ctx

class ProductDetailView(DetailView):
    model = Product
    template_name = 'merchstore-detail.html'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'merchstore-create.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        owner = ProfileModel.Profile.objects.get(user=self.request.user)
        ctx['form'] = ProductForm(
            initial = {
                'owner': owner,
            }
        )
        return ctx


    # def get_initial(self):
    #     initial = super().get_initial()
    #     if self.request.user.is_authenticated:
    #         initial['owner'] = self.request.user.id
    #     return initial


class ProductUpdateView(DetailView):
    model = Product
    template_name = 'merchstore-update.html'


class CartView(DetailView):
    model = Transaction
    template_name = 'merchstore-cart.html'


class TransactionsListView(DetailView):
    model = Transaction
    template_name = 'merchstore-transactions.html'
