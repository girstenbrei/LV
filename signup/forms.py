from django import forms

from signup.models import Participant


class EditParticipant(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['forename', 'lastname', 'born', 'plz', 'location', 'group', 'mail', 'perks', 'additional',
                  'next_station', 'event']
