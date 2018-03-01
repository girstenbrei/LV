from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.views.generic import ListView
from rest_framework import viewsets

from events.forms import EditEvent
from events.models import Event
from events.serializers import EventSerializer


def get_event(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EditEvent(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EditEvent()

    return render(request, 'events/edit_event.html', {'form': form})


class EventList(ListView):
    model = Event
    context_object_name = 'events'


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
