from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML
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
            ), HTML(
                '<my-fieldset v-for="n in range"></my-fieldset>'
            ), ButtonHolder(
                HTML(
                    '<input class="btn btn-secondary" id="button-id-add-questions" name="add-questions" type="button" value="Add set of Questions" v-on:click="add_questionset()">')
                #   Button('add-questions', 'Add set of Questions', css_class='btn-secondary')
            ), ButtonHolder(
                Submit('submit', 'Erstellen')
            )
        )

    def save(self):
        instance = super(EditEvent, self).save(commit=False)
        instance.slug = slugify(str(instance))
        instance.save()
