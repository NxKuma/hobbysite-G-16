from django.urls import path

from .views import ProfileUpdateView, index, RegisterProfileView

urlpatterns = [
    path('profile', ProfileUpdateView.as_view(), name='profile-update'),
    path('', index, name='index'),
    path('register', RegisterProfileView.as_view(), name='register')
]

app_name = 'user_management'