from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django import forms
from django.db import IntegrityError
from django.utils.crypto import get_random_string

from participants.models import Participant


class EditParticipant(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'

        labels = {
            'forename': 'Vorname',
            'lastname': 'Nachname',
        }

    def __init__(self, *args, **kwargs):
        super(EditParticipant, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Persönliche Informationen',
                'forename',
                'lastname',
            ),
            ButtonHolder(
                Submit('submit', 'Anmelden')
            )
        )

    def save(self):
        instance = super(EditParticipant, self).save(commit=False)
        max_tries = 10
        for i in range(max_tries):
            instance.slug = get_random_string()
            try:
                instance.save()
                return instance
            except IntegrityError as e:
                pass
        else:
            raise e
