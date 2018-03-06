from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django import forms
from django.db import IntegrityError
from django.utils.crypto import get_random_string

from participants.models import Participant


class EditParticipant(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['forename', 'lastname', 'born', 'plz', 'location', 'group', 'mail', 'perks', 'additional',
                  'next_station']

        labels = {
            'forename': 'Vorname',
            'lastname': 'Nachname',
            'born': 'Geburtsdatum',
            'plz': 'Postleitzahl',
            'location': 'Wohnort',
            'group': 'Stamm',
            'mail': 'Email Adresse',
            'perks': 'Evtl Bahn Vergünstigungen',
            'additional': 'Weitere Informationen',
            'next_station': 'Nächster Bahnhof',
        }

    def __init__(self, *args, **kwargs):
        super(EditParticipant, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Persönliche Informationen',
                'forename',
                'lastname',
                'born',
            ), Fieldset(
                'Kontaktinformation',
                'location',
                'plz',
                'group',
                'next_station',
                'mail',
            ), Fieldset(
                'Zusätzliche Informationen',
                'perks',
                'additional',
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
