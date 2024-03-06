from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Product, ProductType

class ProductListView(ListView):
    model = Product
    template_name = 'product.html'


# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'product_detail.html'


# class ProductTypeListView(ListView):
#     model = ProductType
#     template_name = 'producttype.html'


class ProductTypeDetailView(DetailView):
    model = ProductType
    template_name = 'producttype.html'
    