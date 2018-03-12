
from .api import SignUpViewSet, EventViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register('api/signup', SignUpViewSet, base_name='signup')
router.register('api/event', EventViewSet, base_name='event')

urlpatterns = router.urls


