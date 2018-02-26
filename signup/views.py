# Create your views here.
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from signup.forms import EditParticipant
from signup.models import Participant


def confirmationMail(participant):
    subject = 'Bestätigung Anmeldung Event'
    body = ''
    mail_addr = participant['mail']
    mail = EmailMessage(subject=subject, body=body, to=[mail_addr])
    mail.send()


def add_participant(request, slug=None):
    if slug:
        form = EditParticipant(instance=get_object_or_404(Participant, slug=slug))
    elif request.method == 'POST':
        form = EditParticipant(request.POST)
        if form.is_valid():
            form.save()
            confirmationMail(form.cleaned_data)
            return HttpResponseRedirect(reverse('thanks', kwargs={'name': form.cleaned_data['forename']}))
    else:
        form = EditParticipant()

    return render(request, 'signup.html', {'form': form})


def thanks(request, name):
    return render(request, 'thanks.html', {'name': name})
