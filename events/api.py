from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.http import HttpResponse
from rest_framework import serializers, viewsets, mixins, filters, status
from rest_framework.decorators import list_route, detail_route, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet


from events.export import event_to_xlsx_buffer
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
        fields = ('id', 'timestamp', 'event', 'user', 'answer_set', 'email')


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
        fields = ('id', 'name', 'description', 'post_address', 'start_datetime', 'end_datetime', 'signup_from', 'signup_to',
                  'slug', 'question_sets', 'signup_set')


class SmallEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('label', )


class QuestionSetViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    serializer_class = QuestionSetSerializer
    queryset = QuestionSet.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = ('label', 'description')


class EventViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    A viewset for viewing and editing signups
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    @detail_route(methods=['GET', 'POST'])
    def signup(self, request, pk):

        event = self.get_object()

        # Check authenticated
        if request.successful_authenticator is None and event.signup_type == Event.SIGNUP_TYPE_AUTH:
            return Response({'state': 'You have to be authenticated to signup to this event'}, status=403)

        user = request.user if request.successful_authenticator else None

        if request.method == 'GET':

            def get_prefilled_value(question_pk):
                return None

            if user:
                # get the last signup of the user for this event
                old_signup = user.signup_set.filter(event=event).first()

                if old_signup:
                    old_answers = old_signup.answer_set.all()

                    def get_prefilled_value(question_pk):
                        answers = old_answers.filter(question__pk=question_pk)
                        if answers.exists():
                            answer = answers.first()
                            concrete_answer = answer.get_child_class()
                            return concrete_answer.get_serialized_value()
                        else:
                            return None
                else:
                    # the user signups for this event for the first time
                    # but maybe we want to fill in data from other events

                    all_old_signups = user.signup_set.all()

                    if all_old_signups.exists():
                        old_answers = Answer.objects.filter(signup__in=all_old_signups)

                        def get_prefilled_value(question_pk):
                            answers = old_answers.filter(question__pk=question_pk).order_by('-signup__timestamp')
                            if answers.exists():
                                answer = answers.first()
                                concrete_answer = answer.get_child_class()
                                return concrete_answer.get_serialized_value()
                            else:
                                return None

            data = dict()
            data['event'] = event.id
            data['change_signup_after_submit'] = event.change_signup_after_submit
            data['multiple_signups_per_person'] = event.multiple_signups_per_person
            # Every survey contains of e-mail field and terms of use
            data['question_sets'] = [
                {
                    'label': 'Generell',
                    'description': 'Die obligatorischen Angaben zu jedem Formular.',
                    'order': -1,
                    'questions': [
                        {
                            "text": 'Wir benötigen deine E-Mail-Adresse, um dir die Pdf-Anmeldung und die postalische Empfangsbestätigung zuzusenden.',
                            "type": Question.MAILANSWER,
                            "required": True,
                            "choices": '',
                            'value': ''  # ToDo: Add the e-mail from the last signups
                        },
                        {
                            "text": 'Stimmst du den AGBs dieses Dienstes zu?',  # ToDo: Write AGBs
                            "type": Question.SINGLECHOICEANSWER,
                            "required": True,
                            "choices": 'Ja, Nein',
                            'value': ''
                        }

                    ]
                }
            ]

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
                        "choices": question.choices,
                        'value': get_prefilled_value(question.pk)
                    })

            return Response(data)

        elif request.method == 'POST':

            with transaction.atomic():
                # check whether terms of use and email are checked
                general_questions = request.data['question_sets'].pop(0)
                e_mail_question = general_questions['questions'][0]
                terms_of_use_question = general_questions['questions'][1]
                try:
                    validate_email(e_mail_question['value'])
                except ValidationError:
                    return Response({'state': 'E-Mail not valid'}, status=403)

                if terms_of_use_question['value'] not in (True, '0'):
                    return Response({'state': 'You have to accept the terms of use.'}, status=403)

                if user:
                    # get the last signup of the user for this event
                    old_signup = user.signup_set.filter(event=event)

                    if old_signup.exists() and (not event.change_signup_after_submit or event.multiple_signups_per_person):
                        return Response({'state': 'No multiple signups or update of submission allowed'}, status=403)

                    if old_signup.exists() and event.change_signup_after_submit:
                        # you can update your submission
                        signup = old_signup.first()
                        # delete old answers
                        signup.answer_set.all().delete()
                    else:
                        signup = SignUp.objects.create(event=event, user=user)
                else:
                    signup = SignUp.objects.create(event=event, user=user)

                # store the signup mail or overwrite the old one
                signup.email = e_mail_question['value']

                for i, question_set in enumerate(event.eventquestionssetrelation_set.all()):
                    for ii, question in enumerate(question_set.question_set.questions.all()):
                        new_value = request.data['question_sets'][i]['questions'][ii]['value']

                        AnswerClass = Question.get_answer_field(question.type)
                        answer = AnswerClass()
                        answer.question = question
                        answer.signup = signup
                        answer.set_serialized_value(new_value)
                        answer.full_clean()
                        answer.save()

                signup.save()

            return Response({'state': 'ok'})

        return Response({'state': 'unsupported method'}, status=405)

    @list_route(methods=['GET', 'POST'])
    @permission_classes((IsAuthenticated,))
    def new(self, request):

        if request.method == 'GET':
            data = dict()
            data['name'] = ''
            data['description'] = ''
            data['post_address'] = ''
            data['start_datetime'] = ''
            data['end_datetime'] = ''
            data['signup_from'] = ''
            data['signup_to'] = ''
            data['signup_to'] = ''
            data['question_sets'] = []
            data['staff_users'] = []
            data['available_question_sets'] = []
            data['available_staff_users'] = [(user.username, user.pk)
                                             for user in User.objects.all().exclude(pk=request.user.pk)]

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
                        "choices": question.choices,
                        "required": question.required
                    })

            return Response(data)

        elif request.method == 'POST':
            with transaction.atomic():

                event = Event()
                event.name = request.data.get('name')
                event.description = request.data.get('description')
                event.post_address = request.data.get('post_address')
                event.start_datetime = request.data.get('start_datetime')
                event.end_datetime = request.data.get('end_datetime')
                event.signup_from = request.data.get('signup_from')
                event.signup_to = request.data.get('signup_to')
                event.signup_type = request.data.get('signup_type')
                event.change_signup_after_submit = request.data.get('change_signup_after_submit')
                event.multiple_signups_per_person = request.data.get('multiple_signups_per_person')
                event.creator = request.user
                event.save()

                # Add the staff users (ToDo: Make removal possible)
                for user_pk in request.data.get('staff_users', list()):
                    event.staff.add(User.objects.get(pk=user_pk))

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
                                choices=question.get('choices', ''),
                                set=new_question_set
                            )

                        EventQuestionsSetRelation.objects.create(
                            event=event,
                            question_set=new_question_set,
                            order=i
                        )

            return Response({'state': 'ok'})

        return Response({'state': 'unsupported method'}, status=405)

    @detail_route(methods=['GET'])
    @permission_classes((IsAuthenticated,))
    def download(self, request, pk):

        event = self.get_object()

        if request.user.pk != event.creator.pk or not request.user.is_superuser:
            return Response({'state': 'Only creator and superuser can access this'}, status=403)

        output = event_to_xlsx_buffer(event)

        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename={}.xlsx".format(event.pk)

        return response


class LoginView(APIView):
    allowed_methods = ['POST']

    def post(self, request, format=None):
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    allowed_methods = ['GET']

    def get(self, request, format=None):
        # simply delete the token to force a login
        if not request.user.is_anonymous:
            logout(request)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)



