from django.db import models


class Participant(models.Model):
    forename = models.CharField(max_length=126)
    lastname = models.CharField(max_length=126)
    born = models.DateField()
    plz = models.CharField(max_length=30)
    location = models.CharField(max_length=254)
    group = models.CharField(max_length=254)
    mail = models.EmailField()
    perks = models.CharField(max_length=254, blank=True)
    additional = models.TextField(blank=True)
    next_station = models.CharField(max_length=254)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return "{}, {}".format(self.forename, self.lastname)
