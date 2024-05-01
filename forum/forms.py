from django import forms

from .models import Thread, Comment


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = '__all__'


class CommentForm(forms.ModelForm):
    entry = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ["entry"]