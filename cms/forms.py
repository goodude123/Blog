from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['author', 'pub_date']
        widgets = {
            'title': forms.Textarea(attrs={
                'rows': 1, 
                'cols': 30,
                'placeholder': 'Title',
            }),
            'content': forms.Textarea(attrs={
                'rows': 40,
                'placeholder': 'Article text',
            })
        }
        