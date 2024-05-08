from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Product, ProductType, Transaction
from .forms import ProductForm, TransactionForm

from user_management import models as ProfileModel

class ProductListView(ListView):
    model = ProductType
    template_name = 'merchstore-list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.session.get('transaction_data'):
            del self.request.session['transaction_data']
        if self.request.user.is_authenticated:
            user = ProfileModel.Profile.objects.get(user=self.request.user)
            products_by_owner = Product.objects.filter(owner=user)
            ctx['products_by_owner'] = products_by_owner
        return ctx


class ProductDetailView(DetailView):
    model = Product
    template_name = 'merchstore-detail.html'

    def get_context_data(self, **kwargs):
        product = self.get_object()
        self.object = product
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            buyer = self.get_current_user() 
            transaction_form = TransactionForm(initial={'product': product, 'buyer':buyer})
            ctx['buyer'] = buyer
        transaction_form = TransactionForm(initial={'product': product})
        ctx['transaction_form'] = transaction_form

        if 'error1' in kwargs.keys():
            ctx['error_msg1'] = 'Amount should not be greater than stock'
        if 'error2' in kwargs.keys():
            ctx['error_msg2'] = 'You cannot buy your products'

        return ctx

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        transaction_data = request.session.get('transaction_data')
        if transaction_data:
            if product.owner.user == self.request.user:
                del request.session['transaction_data']
                return redirect('merchstore:product-list')
            
            buyer = self.get_current_user()
            amount = transaction_data['amount']

            transaction_form = TransactionForm()
            transaction = transaction_form.save(commit=False)
            new_transaction = self.set_transaction(transaction, product, amount, buyer)
            new_transaction.save()
            product.save()

            del request.session['transaction_data']
            return redirect('merchstore:cart')
        else:
            return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        post = request.POST
        product = self.get_object()
        transaction_form = TransactionForm()
        transaction = transaction_form.save(commit=False)
        amount = int(post['amount'])
        if amount > product.stock:
            return self.render_to_response(self.get_context_data(object=product, error=1))
        else:
            product.stock -= amount
            if product.stock <= 0:
                product.status = 'Out of stock'
        if request.user.is_authenticated:
            if product.owner.user == request.user:
                return self.render_to_response(self.get_context_data(object=product, error=2))
            buyer = self.get_current_user()
            new_tansaction = self.set_transaction(transaction, product, amount, buyer)
            new_tansaction.save()
            product.save()
            return redirect('merchstore:cart')
        else:
            request.session['transaction_data'] = {
                'amount': amount,
            }   
            login_url = reverse('login') + '?next=' + request.get_full_path()
            return redirect(login_url)
    
    def set_transaction(self, transaction, product, amount, user):
        transaction.product = product
        transaction.status = 'On cart'
        transaction.buyer = user
        transaction.amount = amount
        return transaction
    
    def get_current_user(self):
        user = ProfileModel.Profile.objects.get(user=self.request.user)
        return user


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'merchstore-create.html'
    
    def get_form(self):
        form = super().get_form(form_class=ProductForm)
        form.fields['owner'].initial = ProfileModel.Profile.objects.get(user=self.request.user)
        return form
    

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'merchstore-update.html'

    def form_valid(self, form):
        form.save()
        product = self.object
        product.status = "Out of Stock" if product.stock == 0 else product.status
        product.save()
        return super().form_valid(form)


class CartView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'merchstore-cart.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = ProfileModel.Profile.objects.get(user=self.request.user)
        transactions_by_buyer = Transaction.objects.filter(buyer=user)
        list_of_sellers = ProfileModel.Profile.objects.all()
        ctx['transactions_by_buyer'] = transactions_by_buyer
        ctx['list_of_sellers'] = list_of_sellers
        return ctx


class TransactionsListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'merchstore-transactions.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = ProfileModel.Profile.objects.get(user=self.request.user)
        products_by_seller = Product.objects.filter(owner=user)
        transactions_of_seller = Transaction.objects.filter(product__in=products_by_seller)
        list_of_buyers = ProfileModel.Profile.objects.all()
        ctx['transactions_of_seller'] = transactions_of_seller
        ctx['list_of_buyers'] = list_of_buyers
        return ctx