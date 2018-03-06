# Register your models here.
from django.contrib import admin

from events.models import Event, Question, Answer, QuestionSet, SignUp

admin.site.register(Event)
admin.site.register(SignUp)
admin.site.register(QuestionSet)
admin.site.register(Question)
admin.site.register(Answer)
