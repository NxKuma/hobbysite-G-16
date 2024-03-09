from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Product, ProductType

class ProductTypeListView(ListView):
    model = ProductType
    template_name = 'product_list.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    