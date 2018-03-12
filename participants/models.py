from django.db import models


class Participant(models.Model):
    forename = models.CharField(max_length=126)
    lastname = models.CharField(max_length=126)

    def __str__(self):
        return "{}, {}".format(self.forename, self.lastname)
