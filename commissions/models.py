from datetime import datetime

from django.db import models
from django.urls import reverse

from user_management import models as user_management_models


class Commission(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        user_management_models.Profile,
        on_delete=models.CASCADE,
        related_name='commission'
    )
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
        related_name='jobs'
    )
    role = models.CharField(max_length=255)
    manpower_required = models.IntegerField()
    ongoing_manpower = models.IntegerField(default=0)
    status = models.CharField(max_length=4, choices=(('open','open'), ('full','full'),), default='open')

    def __str__(self):
        return self.role

    def get_absolute_url(self):
        return reverse('commissions:job', args=[self.pk])

    def update_ongoing_manpower(self):
        accepted = self.applicants.filter(status='accepted').count()
        self.ongiong_manpower = accepted
        self.save()

    class Meta:
        ordering = ['status', '-manpower_required', 'role']


class JobApplication(models.Model):
    job = models.ForeignKey(
        'Job',
        on_delete=models.CASCADE,
        related_name='applicants'
    )
    applicant = models.ForeignKey(
        user_management_models.Profile,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )
    status = models.CharField(max_length=8, choices=(('pending','pending'), ('accepted','accepted'),
        ('rejected','rejected'),), default='pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('commissions:job_application', args=[self.pk])

    class Meta:
        ordering = ['status', '-applied_on']
