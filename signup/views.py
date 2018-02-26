# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from signup.forms import EditParticipant
from signup.models import Participant


def add_participant(request, slug=None):
    if slug:
        form = EditParticipant(instance=get_object_or_404(Participant, slug=slug))
    elif request.method == 'POST':
        form = EditParticipant(request.POST)
        if form.is_valid():
            form.save()
            # redirect_url = urlencode('/thanks-%s'.format(form.cleaned_data['forename']))
            return HttpResponseRedirect(reverse('thanks', kwargs={'name': form.cleaned_data['forename']}))
    else:
        form = EditParticipant()

    return render(request, 'signup.html', {'form': form})


def thanks(request, name):
    return render(request, 'thanks.html', {'name': name})
