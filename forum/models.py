from datetime import datetime

from django.urls import reverse
from django.db import models

from user_management import models as profile_models

class ThreadCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('forum:thread-list', args=[self.pk])

    class Meta:
        ordering = ['name',]    


class Thread(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        profile_models.Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='authors'
    )
    category = models.ForeignKey(
        'ThreadCategory',
        on_delete=models.SET_NULL,
        related_name='threads',
        null = True,
    )
    entry = models.TextField()
    image = models.FileField(upload_to='images/', blank=True)
    created_on = models.DateTimeField(auto_now_add=True) 
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('forum:thread-detail', args=[self.pk])

    class Meta:
        ordering = ['-created_on',]


class Comment(models.Model):
    author = models.ForeignKey(
        profile_models.Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='author'
    )
    thread = models.ForeignKey(
        'Thread',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) 
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on',]