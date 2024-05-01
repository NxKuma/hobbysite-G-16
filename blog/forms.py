from django import forms

from .models import Article, Article_Comment


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Article_Comment
        fields = '__all__'