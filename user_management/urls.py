from django.urls import path

from .views import ProfileUpdateView, index, registerPage

urlpatterns = [
    path('profile', ProfileUpdateView.as_view(), name='profile-update'),
    path('', index, name='index'),
    path('register', registerPage, name='register')
]

app_name = 'user_management'