from django.urls import path

from signup import views

urlpatterns = [
    path('', views.add_participant, name='add_participant'),
    path('list-signup', views.ListParticipants.as_view(template_name='signup_list.html'), name='list_participants'),
    path('thanks-<str:name>', views.thanks, name='thanks'),
    path('<slug:slug>', views.add_participant, name='signup_slug'),
]
