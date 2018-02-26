from django import forms
from django.db import IntegrityError
from django.utils.crypto import get_random_string

from signup.models import Participant


class EditParticipant(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['forename', 'lastname', 'born', 'plz', 'location', 'group', 'mail', 'perks', 'additional',
                  'next_station', 'event']

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
