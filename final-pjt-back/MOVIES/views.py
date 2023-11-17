from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.conf import settings
from .serializers import MovieSerializer, GenreSerializer, ActorSerializer
from .models import Movie, Actor
from datetime import datetime
import requests


# TMDB API People 정보
TMDB_PEOPLE_BASE_URL = 'https://api.themoviedb.org/3/person/popular'

# TMDB API 인기있는 영화
TMDB_POPULAR_BASE_URL = 'https://api.themoviedb.org/3/movie/popular'
TMDB_API_KEY = '7598462be8b94fc1e04d0e6dd30a782e'


# TMDB API Genre 정보
TMDB_GENRE_BASE_URL = 'https://api.themoviedb.org/3/genre/movie/list'


# TMDB API 상세 정보
TMDB_DETAIL_INFO_BASE_URL = 'https://api.themoviedb.org/3/movie/'


# TMDB API 현재 상영중인 영화
TMDB_TRENDING_BASE_URL = 'https://api.themoviedb.org/3/trending/movie/day'


# Create your views here.


# TMDB Genre 정보
@api_view(['GET'])
def api_test_TG(request):
    params = {
            'language': 'ko',
            'api_key': TMDB_API_KEY,
        }
    response = requests.get(TMDB_GENRE_BASE_URL, params=params).json()
    movie_genres = response['genres']

    for genre in movie_genres:
        genre_serializer = GenreSerializer(data=genre)
        if genre_serializer.is_valid(raise_exception=True):
            genre_id = genre['id']
            genre_serializer.save(genre_id=genre_id)
    return JsonResponse({'message': 'Success'})     


# TMDB popular 영화 목록
@api_view(['GET'])
def api_test_TP(request):
    for page in range(1, 501):
        params = {
            'language': 'ko-KR',
            'api_key': TMDB_API_KEY,
            'page': page
        }
        response = requests.get(TMDB_POPULAR_BASE_URL, params=params).json()
        movie_list = response['results']
        print(page)
        for movie in movie_list:
            movie_id = movie['id']
            params = {
                'language': 'ko-KR',
                'api_key': TMDB_API_KEY,
                'append_to_response': 'credits',
            }
            response = requests.get(f'{TMDB_DETAIL_INFO_BASE_URL}{movie_id}', params=params).json()
            print(movie)
            # print(params)
            runtime = response['runtime']
            cast_list = response['credits']['cast']
            for actor in cast_list:
                # 만약 actor가 actor 모델에 존재하면 저장하지 않는다. 조건문 쓰세요. 하는 방법은 알죠? 오아????
                
                if actor['id'] not in Actor.objects.values_list('person_id', flat=True):
                    actor_serializer = ActorSerializer(data=actor)
                    if actor_serializer.is_valid(raise_exception=True):
                        person_id = actor['id']
                        actor_serializer.save(person_id=person_id)
            crew_list = response['credits']['crew']
            if crew_list == []:
                movie['director'] = None
            else:
                for crew in crew_list:
                    if crew['job'] == 'Director':
                        movie['director'] = crew['name']
                        break
                else:
                    movie['director'] = None

            movie['runtime'] = runtime                  
            movie_serializer = MovieSerializer(data=movie)
            
            if movie_serializer.is_valid(raise_exception=True):
                movie_id = movie['id']
                if movie['release_date'] == '':
                    movie['release_date'] = None
                movie_serializer.save(movie_id = movie_id, release_date=movie['release_date'], director=movie['director'])
    return JsonResponse({'message': 'Success'})


  



# TMDB 영화 detail info
@api_view(['GET'])
def api_test_TT(request):
    pass