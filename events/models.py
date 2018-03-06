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
    event = models.ForeignKey(Event)
    participant = models.ForeignKey(Participant)


class QuestionSet(models.Model):
    event = models.ForeignKey(Event)


class Question(models.Model):
    text = models.TextField()
    set = models.ForeignKey(QuestionSet)


class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question)
