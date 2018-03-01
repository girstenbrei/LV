from django.urls import path, include
from rest_framework import routers

from events import views
from events.views import EventList

router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet)

urlpatterns = [
    path('', views.get_event),
    path('<slug:slug>', views.get_event),
    path('list/', EventList.as_view(template_name='event_list.html'), name='eventlist'),
    path('api/', include(router.urls))
]
