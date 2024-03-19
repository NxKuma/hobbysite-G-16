from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Product, ProductType

class ProductListView(ListView):
    model = Product
    template_name = 'products.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    