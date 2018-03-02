from django.urls import path

from events.views import EventList, EventDetail, EventView

urlpatterns = [
    path('', EventView.as_view(), name='event'),
    path('list/', EventList.as_view(template_name='event_list.html'), name='eventlist'),
    path('<slug:slug>', EventDetail.as_view(), name='event_detail'),
]
