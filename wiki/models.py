from datetime import datetime

from django.db import models
from django.urls import reverse

from user_management import models as ProfileModel


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wiki:article-list', args=[self.pk])
    
    class Meta:
        ordering = ['name',]


class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        ProfileModel.Profile,
        on_delete = models.SET_NULL,
        related_name='author'
    )
    article_category = models.ForeignKey(
        'ArticleCategory',
        on_delete = models.SET_NULL,
        related_name='article',
        null = True
    )
    header_image = models.ImageField(upload_to='images/')
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('wiki:article-detail', args=[self.pk])

    class Meta:
        ordering = ['-created_on',]


class Comment(models.Model):
    author = models.ForeignKey(
        ProfileModel.Profile,
        on_delete=models.SET_NULL,
        related_name='comments'
    )
    article = models.ForeignKey(
        'Article',
        on_delete=models.CASCADE,
        related_name='article_comments',
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) 
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on',]
