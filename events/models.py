from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify

from participants.models import Participant

from datetime import datetime
import dateutil.parser


class Event(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    signup_from = models.DateTimeField()
    signup_to = models.DateTimeField(null=True)
    slug = models.SlugField(unique=True)

    SIGNUP_TYPE_PUBLIC = 'pub'
    SIGNUP_TYPE_AUTH = 'aut'

    SIGNUP_TYPES = (
        (SIGNUP_TYPE_PUBLIC, 'Public'),
        (SIGNUP_TYPE_AUTH, 'Authenticated')
    )

    signup_type = models.CharField(max_length=3, choices=SIGNUP_TYPES, default=SIGNUP_TYPE_AUTH)

    # the two of them could be mutual exclusive?
    change_signup_after_submit = models.BooleanField(default=True)
    multiple_signups_per_person = models.BooleanField(default=False)



    question_sets = models.ManyToManyField('QuestionSet', through='EventQuestionsSetRelation', )

    def __str__(self):
        return "{} {}".format(self.name, self.start_datetime.year)

    def _get_unique_slug(self):
        try:
            year = self.start_datetime.year
        except AssertionError:
            year = dateutil.parser.parse(self.start_datetime).year
        slug = slugify("{} {}".format(self.name, year))
        unique_slug = slug
        num = 1
        while Event.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = self._get_unique_slug()
        super().save()


class SignUp(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )


class EventQuestionsSetRelation(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    question_set = models.ForeignKey('QuestionSet', on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()


class QuestionSet(models.Model):
    label = models.TextField(max_length=126)
    description = models.TextField(blank=True)

    DIRECTQ = 'DIR'
    MAILQ = 'MAL'

    TARGET_TYPES = (
        (DIRECTQ, 'Direct'),
        (MAILQ, 'E-Mail')
    )

    target = models.CharField(max_length=8, choices=TARGET_TYPES, default=DIRECTQ)

    def __str__(self):
        return self.label


class AnswerPossibility(models.Model):
    order = models.PositiveSmallIntegerField()
    text = models.CharField(max_length=254)


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    signup = models.ForeignKey('SignUp', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class CharAnswer(Answer):
    MAX_LENGTH = 254

    text = models.CharField(max_length=MAX_LENGTH)


class TextAnswer(Answer):
    MAX_LENGTH = 2046
    text = models.TextField(max_length=MAX_LENGTH)


class DateAnswer(Answer):
    date = models.DateField()


class TimeAnswer(Answer):
    time = models.TimeField()


class MailAnswer(Answer):
    mail = models.EmailField()


class ChoiceAnswer(Answer):
    choice = models.CharField(max_length=254)

    class Meta:
        abstract = True

class SingleChoiceAnswer(ChoiceAnswer):
    pass

class MultiChoiceAnswer(ChoiceAnswer):
    pass


class Question(models.Model):
    text = models.TextField()
    set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, related_name='questions')
    required = models.BooleanField()

    CHARANSWER = 'CHR'
    TEXTANSWER = 'TXT'
    DATEANSWER = 'DAT'
    TIMEANSWER = 'TME'
    MAILANSWER = 'MAL'
    SINGLECHOICEANSWER = 'SLQ'
    MULTICHOICEANSWER = 'MLQ'

    ANSWER_TYPES = (
        (CHARANSWER, 'Characters'),
        (TEXTANSWER, 'Text'),
        (DATEANSWER, 'Date'),
        (TIMEANSWER, 'Time'),
        (MAILANSWER, 'E-Mail'),
        (SINGLECHOICEANSWER, 'Single-Choice'),
        (MULTICHOICEANSWER, 'Multiple Choice'),
    )

    FIELD_MAPPING = {
        CHARANSWER: CharAnswer,
        TEXTANSWER: TextAnswer,
        DATEANSWER: DateAnswer,
        TIMEANSWER: TimeAnswer,
        MAILANSWER: MailAnswer,
        SINGLECHOICEANSWER: SingleChoiceAnswer,
        MULTICHOICEANSWER: MultiChoiceAnswer,
    }

    type = models.CharField(max_length=8, choices=ANSWER_TYPES)

    @classmethod
    def get_answer_field(cls, field_code):
        return cls.FIELD_MAPPING.get(field_code, None)




