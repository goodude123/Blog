from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['author', 'pub_date']
        widgets = {
            'title': forms.Textarea(attrs={
                'placeholder': 'Title',
                'class': 'form-control',
                'aria-label': 'With textarea',
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Article text',
                'class': 'form-control',
                'aria-label': 'With textarea',
            })
        }
        