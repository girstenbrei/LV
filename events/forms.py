from django import forms

from events.models import Event


class MyValidatedForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'start_datetime', 'end_datetime', 'signup_from', 'signup_to']
