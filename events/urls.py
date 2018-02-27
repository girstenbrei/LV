from django.urls import path

from events import views
from events.views import EventList

urlpatterns = [
    path('', views.get_event),
    path('list/', EventList.as_view(template_name='event_list.html'), name='eventlist'),
]
