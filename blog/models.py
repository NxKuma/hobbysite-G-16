from datetime import datetime

from django.db import models
from django.urls import reverse

from user_management import models as profile_models

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:article-list', args=[self.pk])
    
    class Meta:
        ordering = ['name',]


class Article(models.Model):
    title = models.CharField(max_length=255)
    article_author = models.ForeignKey(
        profile_models.Profile,
        on_delete = models.SET_NULL,
        related_name = 'authors',
        null = True
    )
    article_category = models.ForeignKey(
        'ArticleCategory',
        on_delete = models.SET_NULL,
        related_name = 'article_category',
        null = True
    )
    entry = models.TextField()
    image = models.ImageField(upload_to = 'images/')
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article-detail', args=[self.pk])

    class Meta:
        ordering = ['-created_on',]

class Article_Comment(models.Model):
    article_author = models.ForeignKey(
        profile_models.Profile,
        on_delete = models.SET_NULL,
        related_name = 'authors',
        null = True
    )
    thread = models.ForeignKey(
        'article',
        on_delete=models.CASCADE,
        related_name='articles'
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True) 
    updated_on = models.DateTimeField(auto_now = True)
        
    class Meta:
        ordering = ['created_on',]