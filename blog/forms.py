from django import forms

from .models import Article

class SearchForm(forms.Form):
    search_text = forms.CharField(max_length=20, widget=forms.TextInput({
        'class': 'form-control'
    }))


class CreateNewArticle(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'body',)

