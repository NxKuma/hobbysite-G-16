from django.urls import path

from .views import ProductTypeListView, ProductDetailView

urlpatterns = [
    path('merchstore/items', ProductTypeListView.as_view(), name='product-list'),
    path('merchstore/item/<int:pk>', ProductDetailView.as_view(), name='product-detail')
]

app_name = 'merchstore'