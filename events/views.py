# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from events.forms import EditEvent
from events.models import Event


class EventView(CreateView):
    model = Event
    form_class = EditEvent
    success_url = reverse_lazy('event_list')


class EventList(ListView):
    model = Event
    context_object_name = 'events'


class EventDetail(DetailView):
    model = Event
    context_object_name = 'event'
