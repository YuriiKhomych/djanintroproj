from django import forms

from .models import Event


class CreateNewEvent(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('title', 'date', 'from_city', 'destination_city')