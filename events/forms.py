from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django import forms
from django.template.defaultfilters import slugify

from events.models import Event


class EditEvent(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['slug']

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

    def save(self):
        instance = super(EditEvent, self).save(commit=False)
        instance.slug = slugify(str(instance))
        instance.save()
