from django import forms

from .models import Trip


class CreateNewTrip(forms.ModelForm):

    class Meta:
        model = Trip
        fields = ('from_city', 'destination_city', 'date', 'time')