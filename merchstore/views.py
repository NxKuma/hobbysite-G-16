from django.shortcuts import redirect
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

    def get_current_user(self):
        user = ProfileModel.Profile.objects.get(user=self.request.user)
        return user

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        product = self.get_object()
        if self.request.user.is_authenticated:
            buyer = self.get_current_user() 
            transaction_form = TransactionForm(initial={'product': product, 'buyer':buyer})
            ctx['buyer'] = buyer
        transaction_form = TransactionForm(initial={'product': product})
        ctx['transaction_form'] = transaction_form
        return ctx
    
    def post(self, request, *args, **kwargs):
        product = self.get_object()
        buyer = self.get_current_user()
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.product = product
            transaction.buyer = buyer
            product.stock -= transaction.amount
            transaction.save()
            product.save()
            return redirect('merchstore:cart')
        ctx = self.get_context_data(object=product, transaction_form=transaction_form)
        return self.render_to_response(ctx)

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


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'merchstore-update.html'


class CartView(ListView):
    model = Transaction
    template_name = 'merchstore-cart.html'


class TransactionsListView(ListView):
    model = Transaction
    template_name = 'merchstore-transactions.html'
