from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Product, Transaction


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('amount', 'status')