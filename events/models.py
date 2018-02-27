from django.db import models


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    signup_from = models.DateTimeField()
    signup_to = models.DateTimeField()

    def __str__(self):
        return "{} {}".format(self.name, self.start_datetime.year)
