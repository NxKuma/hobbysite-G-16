from django import forms

from .models import Thread


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = '__all__'