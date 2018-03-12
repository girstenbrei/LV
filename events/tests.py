# Create your tests here.
from participants.models import Participant
from .models import Event, QuestionSet, Question, SignUp, TextAnswer, CharAnswer

from django.test import TestCase

from datetime import datetime


class AnimalTestCase(TestCase):
    def setUp(self):
        e = Event.objects.create(name="Testevent",
                             start_datetime=datetime.now(),
                             end_datetime=datetime.now(),
                             signup_from=datetime.now(),
                             signup_to=datetime.now()
                             )

        que_set = QuestionSet.objects.create(
            label="Adressblock",
            description="",
            target=QuestionSet.DIRECTQ
        )

        que_1 = Question.objects.create(
            text="Straße",
            required=True,
            type=Question.CHARANSWER,
            set=que_set
        )

        que_2 = Question.objects.create(
            text="Hausnummer",
            required=True,
            type=Question.CHARANSWER,
            set=que_set
        )

        part = Participant.objects.create(
            forename="Baden",
            lastname="Powell",
            slug="badenpowell2"
        )

        signup = SignUp.objects.create(
            event=e,
            participant=part
        )

        a1 = CharAnswer.objects.create(
            text="Hydepark",
            question=que_1,
            signup=signup
        )

        a2 = CharAnswer.objects.create(
            text="2b",
            question=que_2,
            signup=signup
        )





    def test_add_question_set_to_event(self):
        """Animals that can speak are correctly identified"""
        pass
        # lion = Animal.objects.get(name="lion")
        # cat = Animal.objects.get(name="cat")
        # self.assertEqual(lion.speak(), 'The lion says "roar"')
        # self.assertEqual(cat.speak(), 'The cat says "meow"')