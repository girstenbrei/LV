from django.urls import path

from signup import views

urlpatterns = [
    path('', views.add_participant),
    path('thanks-<str:name>', views.thanks, name='thanks'),
    path('<slug:slug>', views.add_participant),
]
