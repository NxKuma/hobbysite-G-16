from django.urls import path

from .views import ProfileUpdateView, Index

urlpatterns = [
    path('profile', ProfileUpdateView.as_view(), name='profile-update'),
    path('', Index.as_view(), name='index'),
]

app_name = 'user_management'