from django.conf.urls import url
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
#from rest_framework_jwt.views import verify_jwt_token

from .api import SignUpViewSet, EventViewSet, QuestionSetViewSet, LoginView, LogoutView, CheckLoginView

from rest_framework import routers

router = routers.DefaultRouter()
router.register('api/signup', SignUpViewSet, base_name='signup')
router.register('api/event', EventViewSet, base_name='event')
router.register('api/question_set', QuestionSetViewSet, base_name='question_set')

urlpatterns = router.urls

urlpatterns += [
    url(r'^api/logout/', LogoutView.as_view(), name='api_logout'),
    url(r'^api/login/', LoginView.as_view(), name='api_login'),
    url(r'^api/check_login/', CheckLoginView.as_view(), name='api_check_login'),

    url(r'^api/auth/token/obtain/$', TokenObtainPairView.as_view()),
    url(r'^api/auth/token/refresh/$', TokenRefreshView.as_view()),
#    url(r'^api/auth/token/verify/', verify_jwt_token),
]


