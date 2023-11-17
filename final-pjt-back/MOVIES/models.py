from django.db import models


# Create your models here.
# TMDB People 목록
class Actor(models.Model):
    person_id = models.IntegerField()
    name = models.CharField(max_length=100)
    profile_path = models.CharField(max_length=60, blank=True, null=True)


# TMDB Genre 목록
class Genre(models.Model):
    genre_id = models.IntegerField()
    name = models.CharField(max_length=10)


# TMDB popular 영화 목록
class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=100)
    adult = models.BooleanField()
    backdrop_path = models.CharField(max_length=60, blank=True, null=True)
    # max_length=60으로 설정한 이유 : backdrop_path의 가장 긴 문자 길이가 38자
    release_date = models.DateField(blank=True, null=True)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    poster_path = models.CharField(max_length=60, blank=True, null=True)
    popularity = models.FloatField()
    overview = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    runtime = models.IntegerField()
    actors = models.ManyToManyField(Actor)
    director = models.CharField(max_length=50, null=True, blank=True)


    

    
    

