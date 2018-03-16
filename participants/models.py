from django.conf import settings
from django.db import models


class Participant(models.Model):
    forename = models.CharField(max_length=126, blank=True)
    lastname = models.CharField(max_length=126, blank=True)

    def __str__(self):
        return "{}, {}".format(self.forename, self.lastname)
