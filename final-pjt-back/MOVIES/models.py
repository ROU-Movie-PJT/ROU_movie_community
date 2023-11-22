from django.db import models
from django.conf import settings


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


# TMDB Trend 목록
class Trend(models.Model):
    title = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=60, blank=True, null=True)
    genres = models.ManyToManyField(Genre, blank=True)
    release_date = models.DateField(blank=True, null=True)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()


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
    genres = models.ManyToManyField(Genre, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    actors = models.ManyToManyField(Actor, blank=True)
    director = models.CharField(max_length=50, null=True, blank=True)

    like_movie_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_movies', blank=True)  # 영화를 좋아요한 사용자
    dislike_movie_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='dislike_movies', blank=True)  # 영화를 싫어요한 사용자
    watching_movie_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='watching_movies', blank=True)  # 영화를 시청한 사용자
    favorite_movie_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='favorite_movies', blank=True)  # 영화를 찜한 사용자
