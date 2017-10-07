from django import forms
from django.core.exceptions import ValidationError

from .models import Trip, Comment


class SearchForm(forms.Form):
    search_from_city = forms.CharField(max_length=20, widget=forms.TextInput({
        'class': 'form-control'
    }))
    search_destination = forms.CharField(max_length=20, widget=forms.TextInput({
        'class': 'form-control'
    }))


class CreateNewTrip(forms.ModelForm):

    class Meta:
        model = Trip
        fields = ('from_city', 'destination_city', 'date', 'time', 'max_passengers')
        widgets = {

            'from_city': forms.TextInput(attrs={'class': 'geocomplete'}),
            'destination_city': forms.TextInput(attrs={'class': 'geocomplete'}),
            'date': forms.TextInput(attrs={'class': 'datepicker'}),
            'time': forms.TextInput(attrs={'class': 'timepicker'}),
        }


def validate_positive(value):
    if value < 0:
        raise ValidationError('%(value)s is not positive!',
                              params={'value': value})


class CommentForm(forms.ModelForm):

    rating = forms.DecimalField(label="Rating (0-10)")

    class Meta:
        model = Comment
        exclude = ("date", "author", "trip", "edit_date", "edit_amount")
        widgets = {
            "positive": forms.Textarea(attrs={"rows": 4, "cols": 15}),
            "negative": forms.Textarea(attrs={"rows": 4, "cols": 15}),
            "body": forms.Textarea(attrs={"rows": 8, "cols": 15}),
        }


class AddToCartForm(forms.Form):
    counter = forms.IntegerField(widget=forms.NumberInput,
                                 label="Amount",
                                 validators=[validate_positive])
