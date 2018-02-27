from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django import forms

from events.models import Event


class EditEvent(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EditEvent, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Event',
                'name',
                'description',
                'start_datetime',
                'end_datetime'
            ), Fieldset(
                'Anmeldezeitraum',
                'signup_from',
                'signup_to'
            ), ButtonHolder(
                Submit('submit', 'Erstellen')
            )
        )
