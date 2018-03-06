from django.db import models

from participants.models import Participant


class Event(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    signup_from = models.DateTimeField()
    signup_to = models.DateTimeField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return "{} {}".format(self.name, self.start_datetime.year)


class SignUp(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)


class QuestionSet(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    label = models.TextField(max_length=126)

    def __str__(self):
        return self.label


class Question(models.Model):
    text = models.TextField()
    set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)

    CHARANSWER = 'CHR'
    TEXTANSWER = 'TXT'
    DATEANSWER = 'DAT'
    TIMEANSWER = 'TME'
    MAILANSWER = 'MAL'

    ANSWER_TYPES = (
        (CHARANSWER, 'Characters'),
        (TEXTANSWER, 'Text'),
        (DATEANSWER, 'Date'),
        (TIMEANSWER, 'Time'),
        (MAILANSWER, 'E-Mail'),
    )

    type = models.CharField(max_length=8, choices=ANSWER_TYPES)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    signup = models.ForeignKey(SignUp, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class CharAnswer(Answer):
    text = models.CharField(max_length=254)


class TextAnswer(Answer):
    text = models.TextField(max_length=2046)


class DateAnswer(Answer):
    date = models.DateField()


class TimeAnswer(Answer):
    time = models.TimeField()


class MailAnswer(Answer):
    mail = models.EmailField()
