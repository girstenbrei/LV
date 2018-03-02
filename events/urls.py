from django.urls import path

from events.views import EventList, EventDetail, EventView

urlpatterns = [
    path('add/', EventView.as_view(), name='event_add'),
    path('edit/<int:pk>', EventView.as_view(), name='event_edit'),
    path('list/', EventList.as_view(template_name='event_list.html'), name='event_list'),
    path('<slug:slug>', EventDetail.as_view(), name='event_detail'),
]
