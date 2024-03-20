from django.urls import path,include
from .views import ArticleListView, ArticleDetailView
urlpatterns = [
    path('articles', ArticleListView.as_view(), name='article-list'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article-detail')
]

app_name = 'blog'