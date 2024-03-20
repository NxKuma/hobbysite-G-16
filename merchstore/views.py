from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Product, ProductType


class ProductListView(ListView):
    model = ProductType
    template_name = 'merchstore-list.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'merchstore-detail.html'