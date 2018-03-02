from django.urls import path

from events import views
from events.views import EventList, EventDetail

urlpatterns = [
    path('', views.get_event),
    path('<slug:slug>', EventDetail.as_view(), name='event_detail'),
    path('list/', EventList.as_view(template_name='event_list.html'), name='eventlist'),
]
