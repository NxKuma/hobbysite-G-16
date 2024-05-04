from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages

from .models import Product, ProductType, Transaction
from .forms import ProductForm, TransactionForm

from user_management import models as ProfileModel

class ProductListView(ListView):
    model = ProductType
    template_name = 'merchstore-list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = ProfileModel.Profile.objects.get(user=self.request.user)
            products_by_owner = Product.objects.filter(owner=user)
            ctx['products_by_owner'] = products_by_owner
        return ctx

class ProductDetailView(DetailView):
    model = Product
    template_name = 'merchstore-detail.html'

    def get_current_user(self):
        user = ProfileModel.Profile.objects.get(user=self.request.user)
        return user
    
    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        transaction_data = request.session.get('transaction_data')
        if transaction_data:
            user = self.get_current_user()
            # Extract product and amount from session data
            amount = transaction_data['amount']
            status = transaction_data['status']

            # Check if transaction already exists (optional)
            existing_transaction = Transaction.objects.filter(
                product=product,
                amount=amount,
                status=status,
                buyer=None  # Filter for uncompleted transactions
            ).first()

            if existing_transaction:
                # Complete the existing transaction
                existing_transaction.buyer = user
                existing_transaction.save()
            else:
                # Create a new transaction
                transaction = Transaction.objects.create(
                    product=product,
                    amount=amount,
                    status=status,
                    buyer=user,
                )
                product.stock -= transaction.amount
                transaction.save()
                product.save()
                del request.session['transaction_data']
                return redirect('merchstore:cart')
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        product = self.get_object()
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            buyer = self.get_current_user() 
            transaction_form = TransactionForm(initial={'product': product, 'buyer':buyer})
            ctx['buyer'] = buyer
        transaction_form = TransactionForm(initial={'product': product})
        ctx['transaction_form'] = transaction_form
        return ctx

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.product = product
            product.stock -= transaction.amount
            if product.stock <= 0:
                product.status = product.States.OUT_OF_STOCK
            if request.user.is_authenticated:
                buyer = self.get_current_user()
                transaction.buyer = buyer
                transaction.save()
                product.save()
                return redirect('merchstore:cart')
            else:
                # Store transaction details in session
                request.session['transaction_data'] = {
                    'amount': transaction.amount,
                    'status': transaction.status,
                }   
                login_url = reverse('login') + '?next=' + request.get_full_path()
                return redirect(login_url)
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


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'merchstore-update.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form

    def form_valid(self, form):
        form.save()
        product = self.object
        product.status = "Out of Stock" if product.stock == 0 else "Available"
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


class TransactionsListView(ListView):
    model = Transaction
    template_name = 'merchstore-transactions.html'
