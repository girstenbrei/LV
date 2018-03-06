# Register your models here.
from django.contrib import admin

from events.models import Event, Question, QuestionSet, SignUp, CharAnswer, TextAnswer, DateAnswer, TimeAnswer, \
    MailAnswer

admin.site.register(Event)
admin.site.register(SignUp)
admin.site.register(QuestionSet)
admin.site.register(Question)
admin.site.register(CharAnswer)
admin.site.register(TextAnswer)
admin.site.register(DateAnswer)
admin.site.register(TimeAnswer)
admin.site.register(MailAnswer)
