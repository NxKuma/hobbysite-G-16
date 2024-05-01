from django import forms

from .models import Thread, Comment


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].disabled = True


class CommentForm(forms.ModelForm):
    entry = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))

    class Meta:
        model = Comment
        fields = ["entry",]