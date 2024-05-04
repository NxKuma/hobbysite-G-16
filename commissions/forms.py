from django import forms

from .models import JobApplication, Commission


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = []


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = []