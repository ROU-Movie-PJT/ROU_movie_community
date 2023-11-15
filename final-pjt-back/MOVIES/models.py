from django.db import models


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField(null=True, blank=True)
    release_date = models.DateField()
    poster_path = models.TextField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    # genre = models.ManyToManyField(Genre)
