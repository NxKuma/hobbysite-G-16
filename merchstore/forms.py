from django import forms

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
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['product'].disabled = True
    #     self.fields['buyer'].disabled = True