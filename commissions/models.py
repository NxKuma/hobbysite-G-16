from datetime import datetime

from django.db import models
from django.urls import reverse

from user_management.models import Profile


class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=12, choices=(('open','open'), ('full', 'full'), ('completed','completed'),
        ('discontinued','discontinued'),), default='open')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('commissions:commission-detail', args=[self.pk])

    class Meta:
        ordering = ['created_on',]


class Job(models.Model):
    commission = models.ForeignKey(
        'Commission',
        on_delete=models.CASCADE,
        related_name='job'
    )
    role = models.CharField(max_length=255)
    manpower_required = models.IntegerField()
    status = models.CharField(max_length=4, choices=(('open','open'), ('full','full'),), default='open')
    
    def get_absolute_url(self):
        return reverse('commissions:job', args=[self.pk])

    class Meta:
        ordering = ['status', '-manpower_required', 'role']


class JobApplication:
    job = models.ForeignKey(
        'Job',
        on_delete=models.CASCADE,
        related_name='applicant'
    )
    applicant = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='job'
    )
    status = models.CharField(max_length=8, choices=(('pending','pending'), ('accepted','accepted'),
        ('rejected','rejected'),), default='pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('commissions:job_application', args=[self.pk])

    class Meta:
        ordering = ['status', '-applied_on']
