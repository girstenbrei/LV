# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render

from signup.forms import EditParticipant


def add_participant(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EditParticipant(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EditParticipant()

    return render(request, 'events/edit_event.html', {'form': form})
