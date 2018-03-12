from django.db import transaction
from rest_framework import serializers, viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from .models import SignUp, Event, CharAnswer, TextAnswer, Question, Answer, QuestionSet, EventQuestionsSetRelation


class CharFieldSerializer(serializers.Serializer):
    class Meta:
        model = CharAnswer
        fields = '__all__'


class AnswerSerializer(serializers.Serializer):
    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        depth = 1
        fields = '__all__'

class QuestionSetSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = QuestionSet
        fields = ('id', 'label', 'description', 'target', 'questions')


class SignUpSerializer(serializers.ModelSerializer):
    #answer_set = AnswerSerializer(many=True)

    class Meta:
        model = SignUp
        fields = ('id', 'timestamp', 'event', 'participant', 'charanswer_set', 'textanswer_set', 'dateanswer_set',
                  'timeanswer_set', 'mailanswer_set',)


class SignUpViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing signups
    """
    serializer_class = SignUpSerializer
    queryset = SignUp.objects.all()


class EventSerializer(serializers.ModelSerializer):
    question_sets = QuestionSetSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        depth = 1
        fields = ('id', 'name', 'description', 'start_datetime', 'end_datetime', 'signup_from', 'signup_to',
                  'slug', 'question_sets', 'signup_set')




class SmallEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('label', )


def valid_dynamic_field(json_field, value):
    # if json_field.required and (value is None or len(value) == 0):
    #     return False
    # elif json_field.type in 'CHR' and (type(value) is not type("") or len(value) >= CharAnswer.MAX_LENGTH):
    #     return False
    # elif json_field.type == 'TXT' and (type(value) is not type("") or len(value) >= TextAnswer.MAX_LENGTH):
    #     return False
    # elif json_field.type == 'DAT' and (type(value) is not type("") or len(value) >= TextAnswer.MAX_LENGTH):
    #     return False
    # ToDo: this code is damn stupid
    # ToDo: use the validation methods (or you will get injected)
    return True


class EventViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing signups
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    @detail_route(methods=['GET', 'POST'])
    def signup(self, request, pk):

        event = self.get_object()

        if request.method == 'GET':
            data = dict()
            data['event'] = event.id
            data['question_sets'] = []

            for question_set in event.eventquestionssetrelation_set.all():
                data['question_sets'].append({
                    'label': question_set.question_set.label,
                    'description': question_set.question_set.description,
                    'order': question_set.order,
                    'questions': []
                })
                for question in question_set.question_set.questions.all():
                    data['question_sets'][-1]['questions'].append({
                        "text": question.text,
                        "type": question.type,
                        "required": question.required,
                        'value': ''
                    })

            return Response(data)

        elif request.method == 'POST':
            with transaction.atomic():
                # ToDo: add the participant logic
                signup = SignUp.objects.create(event=event)

                for i, question_set in enumerate(event.eventquestionssetrelation_set.all()):
                    for ii, question in enumerate(question_set.question_set.questions.all()):
                        new_value = request.data['question_sets'][i]['questions'][ii]['value']

                        if not valid_dynamic_field(question, new_value):
                            return Response({'error': 'validation error {}'.format(question)})

                        AnswerClass = Question.get_answer_field(question.type)
                        answer = AnswerClass()

                        # don't build a mapping because we might want custom logic
                        if question.type in (Question.CHARANSWER, Question.TEXTANSWER):
                            answer.text = new_value
                        elif question.type == Question.DATEANSWER:
                            answer.date = new_value
                        elif question.type == Question.TIMEANSWER:
                            answer.time = new_value
                        elif question.type == Question.MAILANSWER:
                            answer.mail = new_value
                        elif question.type == Question.MAILANSWER:
                            answer.mail = new_value
                        # ToDo: add choice fields

                        answer.question = question
                        answer.signup = signup
                        answer.save()

            return Response({'state': 'ok'})

        return Response({'state': 'unsupported method'}, status=405)

    @list_route(methods=['GET', 'POST'])
    def new(self, request):

        if request.method == 'GET':
            data = dict()
            data['name'] = ''
            data['description'] = ''
            data['start_datetime'] = ''
            data['end_datetime'] = ''
            data['signup_from'] = ''
            data['signup_to'] = ''
            data['signup_to'] = ''
            data['question_sets'] = []
            data['available_question_sets'] = []

            for question_set in QuestionSet.objects.all():
                data['available_question_sets'].append({
                    'id': question_set.id,
                    'label': question_set.label,
                    'description': question_set.description,
                    'questions': []
                })
                for question in question_set.questions.all():
                    data['available_question_sets'][-1]['questions'].append({
                        "text": question.text,
                        "type": question.type,
                        "required": question.required
                    })

            return Response(data)

        elif request.method == 'POST':
            with transaction.atomic():

                event = Event()
                event.name = request.data.get('name')
                event.description = request.data.get('description')
                event.start_datetime = request.data.get('start_datetime')
                event.end_datetime = request.data.get('end_datetime')
                event.signup_from = request.data.get('signup_from')
                event.signup_to = request.data.get('signup_to')
                event.save()

                for i, question_set in enumerate(request.data['question_sets']):
                    if question_set.get('id', None):
                        EventQuestionsSetRelation.objects.create(
                            event=event,
                            question_set=QuestionSet.objects.get(id=question_set.get('id')),
                            order=i
                        )
                    else:
                        # create the question set with its questions

                        new_question_set = QuestionSet.objects.create(
                            label=question_set.get('label'),
                            description=question_set.get('description')
                        )

                        for ii, question in enumerate(question_set['questions']):
                            # valid types
                            assert question['type'] in Question.FIELD_MAPPING.keys()

                            question = Question.objects.create(
                                text=question.get('text'),
                                type=question.get('type'),
                                required=question.get('required'),
                                set=new_question_set
                            )

                        EventQuestionsSetRelation.objects.create(
                            event=event,
                            question_set=new_question_set,
                            order=i
                        )

            return Response({'state': 'ok'})

        return Response({'state': 'unsupported method'}, status=405)
