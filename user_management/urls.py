from django.urls import path

from .views import ProfileUpdateView, index

urlpatterns = [
    path('profile', ProfileUpdateView.as_view(), name='profile-update'),
    path('', index, name='index'),
]

app_name = 'user_management'