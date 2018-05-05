# Create your tests here.
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from events.api import EventViewSet
from .models import Event, QuestionSet, Question, SignUp, TextAnswer, CharAnswer
from django.test import TestCase
from datetime import datetime
from rest_framework.test import APIRequestFactory, force_authenticate

create_event_json = {
    "question_sets": [
        {"id": 1},
        {"id": 2}
    ],
    "signup_from": "2018-01-01 10:10",
    "signup_to": "2018-01-01 10:10",
    "end_datetime": "2018-01-01 10:10",
    "signup_type": "pub",
    "post_address": "Severinstraße 5 RGB",
    "change_signup_after_submit": False,
    "multiple_signups_per_person": False,
    "name": "API Event 1",
    "start_datetime": "2018-01-01 10:10",
    "description": "Test 1"
}

create_event_json_2 = {
    "name": "API Event 2",
    "signup_to": "2018-01-01 10:10",
    "signup_type": "pub",
    "change_signup_after_submit": False,
    "multiple_signups_per_person": False,
    "question_sets": [

        {
            "description": "Wir brauchen noch ein paar Informationen über dich für die Kursteams.",
            "questions": [
                {
                    "type": "SLQ",
                    "text": "Auf welchen Kurs willst du fahren?",
                    "choices": "KaLu,KfS,KfM,Tilop,Grundkurs Süd,Skout",
                    "required": True
                },
                {
                    "type": "MLQ",
                    "text": "Für den Fall, dass du auf den Grundkurs fährst: Welche Stufe interessiert dich?",
                    "choices": "Wölflingsstufe,Pfadistufe,RR-Stufe,Stafü-Stufe",
                    "required": False
                },
                {
                    "type": "CHR",
                    "text": "Welches Amt hast du gerade bei dir im Stamm?",
                    "required": False
                },
                {
                    "type": "MAL",
                    "text": "Bitte gib deine E-Mail-Adresse an",
                    "required": True
                }
            ],
            "label": "Kursfragen"
        }

    ],
    "description": "test 2",
    "start_datetime": "2018-01-01 10:10",
    "signup_from": "2018-01-01 10:10",
    "end_datetime": "2018-01-01 10:10"
}


class AnimalTestCase(TestCase):
    def setUp(self):
        User.objects.create_superuser('tester', email="test@test.de", password='test')
        self.user = User.objects.get_by_natural_key('tester')

        self.e = Event.objects.create(name="Frühjahrsklausur",
                                      start_datetime=datetime.now(),
                                      end_datetime=datetime.now(),
                                      signup_from=datetime.now(),
                                      signup_to=datetime.now(),
                                      creator=self.user
                                      )

        que_set = QuestionSet.objects.create(
            label="Adressblock",
            description="",
            target=QuestionSet.DIRECTQ
        )

        self.que_1 = Question.objects.create(
            text="Straße",
            required=True,
            type=Question.CHARANSWER,
            set=que_set
        )

        self.que_2 = Question.objects.create(
            text="Hausnummer",
            required=True,
            type=Question.CHARANSWER,
            set=que_set
        )

        self.que_3 = Question.objects.create(
            text="Ort",
            required=True,
            type=Question.CHARANSWER,
            set=que_set
        )

        self.que_4 = Question.objects.create(
            text="PLZ",
            required=True,
            type=Question.CHARANSWER,
            set=que_set
        )

        que_set_2 = QuestionSet.objects.create(
            label="Essgewohnheiten",
            description="",
            target=QuestionSet.DIRECTQ
        )

        self.que_2_1 = Question.objects.create(
            text="Ernährung",
            required=True,
            type=Question.SINGLECHOICEANSWER,
            choices='Fleisch,Vegetarisch,Vegan',
            set=que_set_2
        )

        self.que_2_2 = Question.objects.create(
            text="Allergien",
            required=True,
            type=Question.MULTICHOICEANSWER,
            choices='Nüsse,Hülsenfrüchte,Äpfel',
            set=que_set_2
        )

    def test_programmatic_signup(self):
        event = self.e

        s = SignUp.objects.create(event=event)

        CharAnswer.objects.create(signup=s, question=self.que_1, text='Severinstraße')
        CharAnswer.objects.create(signup=s, question=self.que_2, text='5 RGB')
        CharAnswer.objects.create(signup=s, question=self.que_3, text='München')
        CharAnswer.objects.create(signup=s, question=self.que_4, text='80593')

        CharAnswer.objects.create(signup=s, question=self.que_2_1, text='0')
        CharAnswer.objects.create(signup=s, question=self.que_2_2, text='0,2')

        s = SignUp.objects.last()
        self.assertEqual(s.answer_set.count(), 6)

    def test_api_signup(self):
        event_count = Event.objects.count()

        url = '/api/event/new'
        request = APIRequestFactory().post(url, create_event_json_2, format='json')
        force_authenticate(request, user=self.user)
        view = EventViewSet.as_view({'post': 'new'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Event.objects.count() - 1, event_count)


        event = Event.objects.last()
        old_count = SignUp.objects.count()

        url = '/api/event/{}/signup'.format(event.pk)
        request = APIRequestFactory().get(url, format='json')
        view = EventViewSet.as_view({'get': 'signup'})
        response = view(request, pk=event.pk)
        self.assertEqual(response.status_code, 200)

        payload = response.data
        payload['question_sets'][0]['questions'][0]['value'] = "4"
        payload['question_sets'][0]['questions'][1]['value'] = "0"
        payload['question_sets'][0]['questions'][2]['value'] = "Stammesführung"
        payload['question_sets'][0]['questions'][3]['value'] = "test@pfadfinden.de"

        url = '/api/event/{}/signup'.format(event.pk)
        request = APIRequestFactory().post(url, payload, format='json')
        force_authenticate(request, user=self.user)
        view = EventViewSet.as_view({'post': 'signup'})
        response = view(request, pk=event.pk)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(old_count, SignUp.objects.count() - 1)

    def test_api_signup_invalid_email(self):
        event_count = Event.objects.count()

        url = '/api/event/new'
        request = APIRequestFactory().post(url, create_event_json_2, format='json')
        force_authenticate(request, user=self.user)
        view = EventViewSet.as_view({'post': 'new'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Event.objects.count() - 1, event_count)


        event = Event.objects.last()
        old_count = SignUp.objects.count()

        url = '/api/event/{}/signup'.format(event.pk)
        request = APIRequestFactory().get(url, format='json')
        force_authenticate(request, user=self.user)
        view = EventViewSet.as_view({'get': 'signup'})
        response = view(request, pk=event.pk)
        self.assertEqual(response.status_code, 200)

        payload = response.data
        payload['question_sets'][0]['questions'][0]['value'] = "4"
        payload['question_sets'][0]['questions'][1]['value'] = "0,1"
        payload['question_sets'][0]['questions'][2]['value'] = "Stammesführung"
        payload['question_sets'][0]['questions'][3]['value'] = "test@"

        print(payload)

        url = '/api/event/{}/signup'.format(event.pk)
        request = APIRequestFactory().post(url, payload, format='json')
        force_authenticate(request, user=self.user)
        view = EventViewSet.as_view({'post': 'signup'})

        with self.assertRaises(ValidationError):
            response = view(request, pk=event.pk)

        self.assertEqual(old_count, SignUp.objects.count())


    def test_api_signup_invalid_index_single_choice(self):
        event_count = Event.objects.count()

        url = '/api/event/new'
        request = APIRequestFactory().post(url, create_event_json_2, format='json')
        force_authenticate(request, user=self.user)
        view = EventViewSet.as_view({'post': 'new'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Event.objects.count() - 1, event_count)


        event = Event.objects.last()
        old_count = SignUp.objects.count()

        url = '/api/event/{}/signup'.format(event.pk)
        request = APIRequestFactory().get(url, format='json')
        view = EventViewSet.as_view({'get': 'signup'})
        response = view(request, pk=event.pk)
        self.assertEqual(response.status_code, 200)

        payload = response.data
        payload['question_sets'][0]['questions'][0]['value'] = "9"
        payload['question_sets'][0]['questions'][1]['value'] = "0"
        payload['question_sets'][0]['questions'][2]['value'] = "Stammesführung"
        payload['question_sets'][0]['questions'][3]['value'] = "test@"

        url = '/api/event/{}/signup'.format(event.pk)
        request = APIRequestFactory().post(url, payload, format='json')
        view = EventViewSet.as_view({'post': 'signup'})

        with self.assertRaises(ValueError):
            response = view(request, pk=event.pk)

        self.assertEqual(old_count, SignUp.objects.count())


    def test_api_signup_invalid_index_multiple_choice(self):
        event_count = Event.objects.count()

        url = '/api/event/new'
        request = APIRequestFactory().post(url, create_event_json_2, format='json')
        force_authenticate(request, user=self.user)
        view = EventViewSet.as_view({'post': 'new'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Event.objects.count() - 1, event_count)


        event = Event.objects.last()
        old_count = SignUp.objects.count()

        url = '/api/event/{}/signup'.format(event.pk)
        request = APIRequestFactory().get(url, format='json')
        view = EventViewSet.as_view({'get': 'signup'})
        response = view(request, pk=event.pk)
        self.assertEqual(response.status_code, 200)

        payload = response.data
        payload['question_sets'][0]['questions'][0]['value'] = "0"
        payload['question_sets'][0]['questions'][1]['value'] = "0,1,2,3,4,5,6,7,8"
        payload['question_sets'][0]['questions'][2]['value'] = "Stammesführung"
        payload['question_sets'][0]['questions'][3]['value'] = "test@"

        url = '/api/event/{}/signup'.format(event.pk)
        request = APIRequestFactory().post(url, payload, format='json')
        view = EventViewSet.as_view({'post': 'signup'})

        with self.assertRaises(ValueError):
            response = view(request, pk=event.pk)

        self.assertEqual(old_count, SignUp.objects.count())

    def test_create_new_event(self):
        event_count = Event.objects.count()

        url = '/api/event/new'
        request = APIRequestFactory().post(url, create_event_json_2, format='json')
        force_authenticate(request, user=self.user)
        view = EventViewSet.as_view({'post': 'new'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Event.objects.count()-1, event_count)
