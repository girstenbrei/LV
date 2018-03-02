from django.conf import settings
from django.urls import path

from participants import views

urlpatterns = [
    path('add/', views.add_participant, name='add_participant'),
    path('detail/<int:pk>', views.ParticipantDetailView.as_view(template_name='participant_detail.html'),
         name='participant_detail'),
    path('list', views.ListParticipants.as_view(template_name='signup_list.html'), name='list_participants'),
    path('thanks-<str:name>', views.thanks, name='thanks'),
    path('<slug:slug>', views.add_participant, name='signup_slug'),
]

if settings.DEBUG:
    urlpatterns += [
        path('email/', views.test_mail, name='test_mail')
    ]
