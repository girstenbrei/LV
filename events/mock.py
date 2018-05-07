# Create your tests here.
from django.contrib.auth.models import User

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

    signup = SignUp.objects.create(
        event=e
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


def add_dummy_data_2():
    e = Event.objects.create(name="Oktoberfest3",
                         start_datetime=datetime.now(),
                         end_datetime=datetime.now(),
                         signup_from=datetime.now(),
                         signup_to=datetime.now(),
                             creator=User.objects.first(),
                             signup_type=Event.SIGNUP_TYPE_PUBLIC
                         )

    que_set = QuestionSet.objects.create(
        label="TestQuestionSet",
        description="Dieses Set enthält alle Komponenten",
        target=QuestionSet.DIRECTQ
    )

    que_1 = Question.objects.create(
        text="Straße",
        required=True,
        type=Question.CHARANSWER,
        set=que_set
    )

    que_2 = Question.objects.create(
        text="E-Mail",
        required=True,
        type=Question.MAILANSWER,
        set=que_set
    )

    que_3 = Question.objects.create(
        text="Datum",
        required=True,
        type=Question.DATEANSWER,
        set=que_set
    )

    que_4 = Question.objects.create(
        text="Uhrzeit",
        required=True,
        type=Question.TIMEANSWER,
        set=que_set
    )

    que_5 = Question.objects.create(
        text="Motivationsschreiben",
        required=True,
        type=Question.TEXTANSWER,
        set=que_set
    )

    que_6 = Question.objects.create(
        text="Bundestagswahl",
        required=True,
        type=Question.SINGLECHOICEANSWER,
        set=que_set,
        choices='SPD,CDU/CSU,Die Grünen,Die Piraten'
    )

    que_6 = Question.objects.create(
        text="Einkaufsliste",
        required=True,
        type=Question.MULTICHOICEANSWER,
        set=que_set,
        choices='Moet,Champagner,Kaviar,Petersilie,Caprisonne'
    )


    EventQuestionsSetRelation.objects.create(
        event=e,
        question_set=que_set,
        order=0
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

create_event_json_2 = """
{
    "name": "API Event 2",
    "signup_to": "2018-01-01 10:10",
    "question_sets": [

	{
            "id": 1
        },

	{
            "description": "Wir möchten die Küche planen",
            "questions": [
                {
                    "type": "CHR",
                    "text": "Wie viel esse ich? (1=wenig...5=viel)",
                    "required": false
                },
                {
                    "type": "CHR",
                    "text": "Ich esse Fleisch",
                    "required": true
                }
            ],
            "label": "Essgewohnheiten"
        }

	],
    "description": "test 2",
    "start_datetime": "2018-01-01 10:10",
    "signup_from": "2018-01-01 10:10",
    "end_datetime": "2018-01-01 10:10"
}
"""
