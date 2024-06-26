from django.urls import path

from .views import CommissionListView, CommissionDetailView, CommissionUpdateView, CommissionCreateView

urlpatterns = [
	path('list', CommissionListView.as_view(), name='commission'),
	path('detail/<int:pk>', CommissionDetailView.as_view(), name='commission-detail'),
	path('add', CommissionCreateView.as_view(), name='commission-create'),
	path('<int:pk>/edit', CommissionUpdateView.as_view(), name='commission-update')
]

app_name = 'commissions'