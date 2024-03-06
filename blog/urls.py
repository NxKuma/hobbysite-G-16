from django.contrib import admin
from django.urls import path,include
from .views import index, task_list, task_detail, TaskListView, TaskDetailView

urlpatterns = [
    path('blog/articles', TaskListView.as_view(), name='article-list'),
    path('<int:pk>/detail', TaskDetailView.as_view(), name='task-detail')
]

app_name = 'blog'