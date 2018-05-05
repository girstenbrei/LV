from django.conf.urls import url

from .api import SignUpViewSet, EventViewSet, QuestionSetViewSet, LoginView, LogoutView

from rest_framework import routers

router = routers.DefaultRouter()
router.register('api/signup', SignUpViewSet, base_name='signup')
router.register('api/event', EventViewSet, base_name='event')
router.register('api/question_set', QuestionSetViewSet, base_name='question_set')

urlpatterns = router.urls

urlpatterns += [
    url(r'^api/logout/', LogoutView.as_view(), name='api_logout'),
    url(r'^api/login/', LoginView.as_view(), name='api_login'),
]


