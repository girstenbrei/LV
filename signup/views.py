# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from signup.forms import EditParticipant
from signup.models import Participant


def add_participant(request, slug=None):
    if slug:
        form = EditParticipant(instance=get_object_or_404(Participant, slug=slug))
    elif request.method == 'POST':
        form = EditParticipant(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = EditParticipant()

    return render(request, 'events/edit_event.html', {'form': form})
