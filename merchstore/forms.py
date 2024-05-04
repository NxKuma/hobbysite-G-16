from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Product, Transaction


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].disabled = True


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('amount', 'status')

    # def save(self, commit=True):
    #     transaction = super().save(commit=False)
    #     if commit:
    #         transaction.save()

    #         # Check if user is authenticated
    #         if self.user.is_authenticated:
    #             # Redirect to CartView
    #             return HttpResponseRedirect(reverse('merchstore:cart'))
    #         else:
    #             # Redirect to login page
    #             return HttpResponseRedirect(reverse('login'))  # Update 'login' with your actual login URL

        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['product'].disabled = True
    #     self.fields['buyer'].disabled = True