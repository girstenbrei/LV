# Create your views here.
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import ListView, DetailView

from events.models import Event
from participants.forms import EditParticipant
from participants.models import Participant


def confirmationMail(host, participant, slug, event_name):
    subject = 'Bestätigung Anmeldung {}'.format(event_name)
    reverse_slug = reverse('signup_slug', kwargs={'slug': slug})
    body = render_to_string('signup-mail.html', {'participant': participant, 'slug': reverse_slug, 'host': host})
    send_mail(
        subject=subject,
        recipient_list=[participant['mail']],
        from_email=settings.EMAIL_FROM,
        message="",
        html_message=body
    )


def add_participant(request, slug=None):
    if slug:
        form = EditParticipant(instance=get_object_or_404(Participant, slug=slug))
    elif request.method == 'POST':
        form = EditParticipant(request.POST)
        if form.is_valid():
            instance = form.save()
            confirmationMail(request.get_host(), form.cleaned_data, instance.slug, instance.event.name)
            return HttpResponseRedirect(reverse('thanks', kwargs={'name': form.cleaned_data['forename']}))
    else:
        event = request.GET.get('event', '')
        form = EditParticipant(initial={'event': event})

    return render(request, 'signup.html', {'form': form})


def thanks(request, name):
    return render(request, 'thanks.html', {'name': name})


class ListParticipants(ListView):
    model = Participant
    context_object_name = 'participants'

    def get_queryset(self):
        event_id = self.request.GET.get('event', '')
        self.event = get_object_or_404(Event, id=event_id)
        return Participant.objects.filter(event=self.event)


class ParticipantDetailView(DetailView):
    model = Participant


def test_mail(request):
    context = {
        'participant': {
            'forename': "Alex",
            'lastname': 'Jones',
            'born': 'jep',
            'plz': '81377',
            'event': {
                'name': 'Testevent'
            }
        }
    }
    return render(request, 'signup-mail.html', context)
