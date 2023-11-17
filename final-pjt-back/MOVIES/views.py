from datetime import date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework import status
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import *
from .models import Movie, Actor
# from datetime import datetime
import requests


# movies = Movie.objects.annotate(
#         like_movie_users_count=Count('like_movie_users', distinct=True), # 좋아요한 사용자 수
#         dislike_movie_users_count=Count('dislike_movie_users', distinct=True), # 싫어요한 사용자 수
#         watching_movie_users_count=Count('watching_movie_users', distinct=True), # 시청중인 사용자 수
#         favorite_movie_users_count=Count('favorite_movie_users', distinct=True), # 찜한 사용자 수
#         review_movie_count=Count('write_movie_review', distinct=True)) # 리뷰글의 수)

# User = get_user_model()

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


# TMDB 영화 트렌드
@api_view(['GET'])
def api_test_TT(request):
    params = {
        'language': 'ko',
        'api_key': TMDB_API_KEY,
    }
    response = requests.get(TMDB_TRENDING_BASE_URL, params=params).json()
    movie_trend = response['results']

    for movie in movie_trend:
        trend_serializer = TrendSerializer(data=movie)
        if trend_serializer.is_valid(raise_exception=True):
            trend_serializer.save()
    return JsonResponse({'message': 'Success'})           

import json

# TMDB popular 영화 목록
@api_view(['GET'])
def api_test_TP(request):
    for page in range(1, 501):
        params = {
            'language': 'ko-KR',
            'api_key': TMDB_API_KEY,
            'page': page
        }
        try:
            response = requests.get(TMDB_POPULAR_BASE_URL, params=params).json()
            movie_list = response['results']
            
            for movie in movie_list:
                movie_id = movie['id']
                params = {
                    'language': 'ko-KR',
                    'api_key': TMDB_API_KEY,
                    'append_to_response': 'credits',
                }
                try:
                    response = requests.get(f'{TMDB_DETAIL_INFO_BASE_URL}{movie_id}', params=params).json()
                    runtime = response['runtime']
                    cast_list = response['credits']['cast']
                    for actor in cast_list:
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
                except json.JSONDecodeError as e:
                    pass        
        except json.JSONDecodeError as e:
            pass
               
    return JsonResponse({'message': 'Success'})


# 메인 영화 조회
# 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능 
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def movies_main(request):
    main_movies = movies.filter(release_date__lte=date.today()).order_by('-release_date', '-vote_average')[:20]
    serializer = MovieSerializer(main_movies, Many=True)
    return Response(serializer.data)
  

# 필터링된 영화 정보(장르 포함)
def movie_sort(request):
    pass


# 단일 영화 조회
# 모든 사용자 GET가능 
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def movie_detail(request, movie_pk):
    movie = movies.get(pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


# 영화별 게시글 조회
def movie_review(request):
    pass


# # 영화 좋아요 등록 및 해제(좋아요 수까지 출력)
# # 인증된 사용자만 권한 허용
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def movie_like(request, movie_pk):
#     movie = get_object_or_404(Movie, pk=movie_pk)
#     user = request.user

#     # 해제
#     if movie.like_movie_users.filter(pk=user.pk).exists():
#         movie.like_movie_users.remove(user)

#     # 등록
#     else:
#         movie.like_movie_users.add(user)

#     serializer = MovieLikeSerializer(movie) 

#     like_movie_register = {
#         'id' : serializer.data.get('id'),
#         'like_movie_users_count' : movie.like_movie_users.count(),
#         'like_movie_users' : serializer.data.get('like_movie_users'),
#     }
#     return JsonResponse(like_movie_register)   

# # 영화 싫어요 등록 및 해제(싫어요 수까지 출력)
# # 인증된 사용자만 권한 허용
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def movie_dislike(request, movie_pk):
#     movie = get_object_or_404(Movie, pk=movie_pk)
#     user = request.user

#     # 해제
#     if movie.dislike_movie_users.filter(pk=user.pk).exists():
#         movie.dislike_movie_users.remove(user)

#     # 등록
#     else:
#         movie.dislike_movie_users.add(user)

#     serializer = MovieDisLikeSerializer(movie) 

#     dislike_movie_register = {
#         'id' : serializer.data.get('id'),
#         'like_movie_users_count' : movie.dislike_movie_users.count(),
#         'like_movie_users' : serializer.data.get('dislike_movie_users'),
#     }
#     return JsonResponse(dislike_movie_register)     


# # 시청 중인 영화 등록 및 해제(시청 수까지 출력)
# # 인증된 사용자만 권한 허용
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def movie_watching(request, movie_pk):
#     movie = get_object_or_404(Movie, pk=movie_pk)
#     user = request.user

#     # 해제
#     if movie.watching_movie_users.filter(pk=user.pk).exists():
#         movie.watching_movie_users.remove(user)

#     # 등록
#     else:
#         movie.watching_movie_users.add(user)

#     serializer = MovieWatchingSerializer(movie) 

#     watching_movie_register = {
#         'id' : serializer.data.get('id'),
#         'watching_movie_users_count' : movie.watching_movie_users.count(),
#         'watching_movie_users' : serializer.data.get('watching_movie_users'),
#     }
#     return JsonResponse(watching_movie_register)


# # 찜한 영화 등록 및 해제(시청 수까지 출력)
# # 인증된 사용자만 권한 허용
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def movie_favorite(request, movie_pk):
#     movie = get_object_or_404(Movie, pk=movie_pk)
#     user = request.user

#     # 해제
#     if movie.favorite_movie_users.filter(pk=user.pk).exists():
#         movie.favorite_movie_users.remove(user)

#     # 등록
#     else:
#         movie.favorite_movie_users.add(user)

#     serializer = MovieFavoriteSerializer(movie) 

#     favorite_movie_register = {
#         'id' : serializer.data.get('id'),
#         'favorite_movie_users_count' : movie.favorite_movie_users.count(),
#         'favorite_movie_users' : serializer.data.get('favorite_movie_users'),
#     }
#     return JsonResponse(favorite_movie_register)


# 박스오피스 인기 영화 조회
# 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def movie_trend(request):
    movie = get_object_or_404(Trend)
    serializer = TrendSerializer(movie)
    return Response(serializer.data)


# (추천)장르별 추천 영화 조회
def movie_genre(request):
    pass


# (추천)역대급 영화
def best_movie(request):
    pass


# (추천)날씨별 추천 영화
# (추천)날씨별 추천 영화
def for_weather(request):
    pass
