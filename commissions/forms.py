from django import forms

from .models import JobApplication, Commission, Job


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['author'].disabled=True

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['role', 'manpower_required']


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = []