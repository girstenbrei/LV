# Create your tests here.
from participants.models import Participant
from .models import Event, QuestionSet, Question, SignUp, TextAnswer, CharAnswer, EventQuestionsSetRelation

from datetime import datetime


def add_dummy_data():
    e = Event.objects.create(name="Testevent",
                         start_datetime=datetime.now(),
                         end_datetime=datetime.now(),
                         signup_from=datetime.now(),
                         signup_to=datetime.now()
                         )

    que_set = QuestionSet.objects.create(
        label="Adressblock",
        description="",
        target=QuestionSet.DIRECTQ,
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

    que_set_2 = QuestionSet.objects.create(
        label="Anreise und Abreise",
        description="Wann du kommst habe ich gefragt!",
        target=QuestionSet.DIRECTQ,
    )

    que_2_1 = Question.objects.create(
        text="Von welchem Bahnhof aus willst du starten?",
        required=True,
        type=Question.CHARANSWER,
        set=que_set_2
    )

    que_2_2 = Question.objects.create(
        text="Bei welchem Bahnhof willst du abgesetzt werden?",
        required=True,
        type=Question.CHARANSWER,
        set=que_set_2
    )

    part = Participant.objects.create(
        forename="Baden",
        lastname="Powell"
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

    a3 = CharAnswer.objects.create(
        text="München Hbf",
        question=que_2_1,
        signup=signup
    )

    a4 = CharAnswer.objects.create(
        text="Würzburg Hbf",
        question=que_2_2,
        signup=signup
    )

    EventQuestionsSetRelation.objects.create(
        event=e,
        question_set=que_set,
        order=1
    )

    EventQuestionsSetRelation.objects.create(
        event=e,
        question_set=que_set_2,
        order=2
    )


create_event_json = """
{
    "question_sets": [
		{"id": 1},
		{"id": 2},
		{"id": 7}
	],
    "signup_from": "2018-01-01 10:10",
    "signup_to": "2018-01-01 10:10",
    "end_datetime": "2018-01-01 10:10",
    "name": "API Event 1",
    "start_datetime": "2018-01-01 10:10",
    "description": "Test 1"
}
"""


