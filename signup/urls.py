from django.urls import path

from signup import views

urlpatterns = [
    path('', views.get_event),
]
