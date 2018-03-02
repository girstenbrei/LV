# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

from events.forms import EditEvent
from events.models import Event


class EventView(FormView):
    template_name = 'events/edit_event.html'
    form_class = EditEvent
    success_url = reverse_lazy('eventlist')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EventList(ListView):
    model = Event
    context_object_name = 'events'

class EventDetail(DetailView):
    model = Event
    context_object_name = 'event'