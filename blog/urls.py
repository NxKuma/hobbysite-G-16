from django.urls import path,include
from .views import ArticleListView, ArticleDetailView
urlpatterns = [
    path('blog/articles', ArticleListView.as_view(), name='article-list'),
    path('<int:pk>/detail', ArticleDetailView.as_view(), name='task-detail')
]

app_name = 'blog'