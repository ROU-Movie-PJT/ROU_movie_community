from datetime import date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework import status
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Count
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from .serializers import *
from .models import *
from datetime import datetime
import requests
import json
from asgiref.sync import async_to_sync, sync_to_async
import aiohttp
import asyncio
import logging  # 추가: 로깅을 위한 임포트
from rest_framework.views import APIView  # 추가
from rest_framework.response import Response


User = get_user_model()


movies = Movie.objects.annotate(
    like_movie_users_count=Count(
        'like_movie_users', distinct=True),  # 좋아요한 사용자 수
    dislike_movie_users_count=Count(
        'dislike_movie_users', distinct=True),  # 싫어요한 사용자 수
    watching_movie_users_count=Count(
        'watching_movie_users', distinct=True),  # 시청중인 사용자 수
    favorite_movie_users_count=Count(
        'favorite_movie_users', distinct=True),  # 찜한 사용자 수
    review_movie_count=Count('write_movie_review', distinct=True),  # 리뷰글의 수
)


# TMDB API 인기있는 영화
TMDB_POPULAR_BASE_URL = 'https://api.themoviedb.org/3/movie/popular'
# TMDB API Genre 정보
TMDB_GENRE_BASE_URL = 'https://api.themoviedb.org/3/genre/movie/list'
# TMDB API 상세 정보
TMDB_DETAIL_INFO_BASE_URL = 'https://api.themoviedb.org/3/movie/'
# TMDB API 현재 상영중인 영화
TMDB_TRENDING_BASE_URL = 'https://api.themoviedb.org/3/trending/movie/day'
# TMDB_API_KEY = '7598462be8b94fc1e04d0e6dd30a782e'
TMDB_API_KEY = '49d792ca8a7053508d689eedb328f369'


# Create your views here.

@permission_classes([IsAuthenticatedOrReadOnly])
class FetchTMDBPopularMovies(APIView):

    def get(self, request, format=None):
        async_to_sync(self.fetch_all_movies)()  # async_to_sync를 사용하여 비동기 함수 호출
        return Response({'message': 'Success'})

    async def fetch_all_movies(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_movie_page(session, page)
                     for page in range(1, 501)]
            await asyncio.gather(*tasks)

    async def fetch_movie_page(self, session, page):
        params = {
            'language': 'ko-KR',
            'api_key': TMDB_API_KEY,
            'page': page
        }
        try:
            response = await session.get(TMDB_POPULAR_BASE_URL, params=params)
            data = await response.json()
            movie_list = data['results']
            await asyncio.gather(*[self.process_movie(movie) for movie in movie_list])
        except json.JSONDecodeError as e:
            logging.error(f"JSON decoding error: {e}")

    async def process_movie(self, movie):
        await sync_to_async(self.save_movie)(movie)

    def save_movie(self, movie):
        movie_id = movie['id']
        movie_data = {
            'like_movie_users_count': 0,
            'dislike_movie_users_count': 0,
            'watching_movie_users_count': 0,
            'favorite_movie_users_count': 0,
        }
        # Update movie_data with the actual movie data
        movie_data.update(movie)
        movie_serializer = MovieSerializer(data=movie_data)
        if movie_serializer.is_valid(raise_exception=True):
            if movie['release_date'] == '':
                movie['release_date'] = None
            movie_serializer.save(
                movie_id=movie_id, release_date=movie['release_date'])


@permission_classes([IsAuthenticatedOrReadOnly])
class UpdateTMDBMovieDetails(APIView):

    def get(self, request, format=None):
        async_to_sync(self.update_movies_with_additional_details)()
        return Response({'message': 'Movie details updated successfully'})

    async def update_movies_with_additional_details(self):
        movies = await sync_to_async(list)(Movie.objects.all())
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.update_movie_detail(session, movie) for movie in movies])

    async def update_movie_detail(self, session, movie):
        movie_id = movie.movie_id
        detail_url = f'{TMDB_DETAIL_INFO_BASE_URL}{movie_id}'
        params = {
            'language': 'ko-KR',
            'api_key': TMDB_API_KEY,
            'append_to_response': 'credits',
        }

        response = await session.get(detail_url, params=params)
        details = await response.json()

        # Check if the required data is available
        if 'credits' in details and 'genres' in details:
            await sync_to_async(self.save_movie_details)(movie, details)
        else:
            logging.error(
                f"Required data missing in API response for movie ID {movie_id}")

    def save_movie_details(self, movie, details):
        movie.runtime = details.get('runtime')
        director = next((crew['name'] for crew in details['credits']
                        ['crew'] if crew['job'] == 'Director'), None)
        movie.director = director

        # Update actors and genres
        actors_data = details['credits']['cast'] if 'credits' in details else [
        ]
        genres_data = details['genres'] if 'genres' in details else []
        actors = [self.update_or_create_actor(actor) for actor in actors_data]
        genres = [self.update_or_create_genre(genre) for genre in genres_data]

        movie.actors.set(actors)
        movie.genres.set(genres)

        movie.save()

    def update_or_create_actor(self, actor_data):
        actor, _ = Actor.objects.update_or_create(
            person_id=actor_data['id'],
            defaults={
                'name': actor_data['name'], 'profile_path': actor_data.get('profile_path')}
        )
        return actor

    def update_or_create_genre(self, genre_data):
        genre, _ = Genre.objects.update_or_create(
            genre_id=genre_data['id'],
            defaults={'name': genre_data['name']}
        )
        return genre

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
@permission_classes([IsAuthenticatedOrReadOnly])
def api_test_TT(request):
    Trend.objects.all().delete()

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


# # TMDB popular 영화 목록
# @api_view(['GET'])
# def api_test_TP(request):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     result = loop.run_until_complete(fetch_all_movies())
#     return JsonResponse({'message': 'Success'})


# async def fetch_all_movies():
#     async with aiohttp.ClientSession() as session:
#         for page in range(1, 501):
#             await fetch_movie_page(session, page)


# async def fetch_movie_page(session, page):
#     params = {
#         'language': 'ko-KR',
#         'api_key': TMDB_API_KEY,
#         'page': page
#     }
#     response = await session.get(TMDB_POPULAR_BASE_URL, params=params)
#     data = await response.json()
#     movie_list = data['results']
#     await fetch_movie_details(session, movie_list)


# async def fetch_movie_details(session, movie_list):
#     for movie in movie_list:
#         await process_movie(session, movie)


# async def check_and_save_actor(actor):
#     if actor['id'] not in await sync_to_async(Actor.objects.values_list)('person_id', flat=True):
#         actor_serializer = ActorSerializer(data=actor)
#         if actor_serializer.is_valid(raise_exception=True):
#             await sync_to_async(actor_serializer.save)(person_id=actor['id'])


# async def process_movie(session, movie):
#     movie_id = movie['id']
#     params = {
#         'language': 'ko-KR',
#         'api_key': TMDB_API_KEY,
#         'append_to_response': 'credits',
#     }
#     response = await session.get(f'{TMDB_DETAIL_INFO_BASE_URL}{movie_id}', params=params)
#     movie_detail = await response.json()

#     # 동기 함수로 분리된 ORM 작업 호출
#     await sync_to_async(process_movie_orm, thread_sensitive=True)(movie, movie_detail)


# def process_movie_orm(movie, movie_detail):
#     # 영화 상세 정보 처리
#     runtime = movie_detail['runtime']
#     cast_list = movie_detail['credits']['cast']
#     for actor in cast_list:
#         if actor['id'] not in Actor.objects.values_list('person_id', flat=True):
#             actor_serializer = ActorSerializer(data=actor)
#             if actor_serializer.is_valid(raise_exception=True):
#                 actor_serializer.save(person_id=actor['id'])

#     crew_list = movie_detail['credits']['crew']
#     if not crew_list:
#         movie['director'] = None
#     else:
#         movie['director'] = next(
#             (crew['name'] for crew in crew_list if crew['job'] == 'Director'), None)

#     movie['runtime'] = runtime
#     movie_serializer = MovieSerializer(data=movie)

#     if movie_serializer.is_valid(raise_exception=True):
#         movie_id = movie['id']
#         if movie['release_date'] == '':
#             movie['release_date'] = None
#         movie_serializer.save(
#             movie_id=movie_id, release_date=movie['release_date'], director=movie['director'])


# 메인 영화 조회
# 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def movies_main(request):
    main_movies = movies.filter(release_date__lte=date.today()).order_by(
        '-release_date', '-vote_average')[:20]
    serializer = MovieSerializer(main_movies, many=True)
    print(main_movies)
    return Response(serializer.data)


# 단일 영화 조회
# 모든 사용자 GET가능
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def movie_detail(request, movie_pk):
    movie = movies.get(pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


# # 영화별 게시글 조회
@api_view(['GET'])
# 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
@permission_classes([IsAuthenticatedOrReadOnly])
def movie_review(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    serializer = MovieReviewSerializer(movie)
    return Response(serializer.data)

# 영화 좋아요 등록 및 해제(좋아요 수까지 출력)
# 인증된 사용자만 권한 허용


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user

    # 해제
    if movie.like_movie_users.filter(pk=user.pk).exists():
        movie.like_movie_users.remove(user)

    # 등록
    else:
        movie.like_movie_users.add(user)

    serializer = MovieLikeSerializer(movie)

    like_movie_register = {
        'id': serializer.data.get('id'),
        'like_movie_users_count': movie.like_movie_users.count(),
        'like_movie_users': serializer.data.get('like_movie_users'),
    }
    return JsonResponse(like_movie_register)

# 영화 싫어요 등록 및 해제(싫어요 수까지 출력)
# 인증된 사용자만 권한 허용


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_dislike(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user

    # 해제
    if movie.dislike_movie_users.filter(pk=user.pk).exists():
        movie.dislike_movie_users.remove(user)

    # 등록
    else:
        movie.dislike_movie_users.add(user)

    serializer = MovieDisLikeSerializer(movie)

    dislike_movie_register = {
        'id': serializer.data.get('id'),
        'dislike_movie_users_count': movie.dislike_movie_users.count(),
        'dislike_movie_users': serializer.data.get('dislike_movie_users'),
    }
    return JsonResponse(dislike_movie_register)


# 시청 중인 영화 등록 및 해제(시청 수까지 출력)
# 인증된 사용자만 권한 허용
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_watching(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user

    # 해제
    if movie.watching_movie_users.filter(pk=user.pk).exists():
        movie.watching_movie_users.remove(user)

    # 등록
    else:
        movie.watching_movie_users.add(user)

    serializer = MovieWatchingSerializer(movie)

    watching_movie_register = {
        'id': serializer.data.get('id'),
        'watching_movie_users_count': movie.watching_movie_users.count(),
        'watching_movie_users': serializer.data.get('watching_movie_users'),
    }
    return JsonResponse(watching_movie_register)


# 찜한 영화 등록 및 해제(시청 수까지 출력)
# 인증된 사용자만 권한 허용
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_favorite(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user

    # 해제
    if movie.favorite_movie_users.filter(pk=user.pk).exists():
        movie.favorite_movie_users.remove(user)

    # 등록
    else:
        movie.favorite_movie_users.add(user)

    serializer = MovieFavoriteSerializer(movie)

    favorite_movie_register = {
        'id': serializer.data.get('id'),
        'favorite_movie_users_count': movie.favorite_movie_users.count(),
        'favorite_movie_users': serializer.data.get('favorite_movie_users'),
    }
    return JsonResponse(favorite_movie_register)


# 박스오피스 인기 영화 조회
# 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def movie_trend(request):
    movies = get_list_or_404(Trend, pk__in=range(1, 21))
    serializer = TrendSerializer(movies, many=True)
    return Response(serializer.data)


# # (추천)장르별 추천 영화 조회
@api_view(['GET'])
# 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
@permission_classes([IsAuthenticatedOrReadOnly])
def movie_genre(request, genre_id):
    genre_movie = movies.filter(
        genres=genre_id,
        release_date__lte=date.today()).order_by('?')[:10]
    serializer = MovieSerializer(genre_movie, many=True)
    return Response(serializer.data)


# 필터링된 영화 정보
@api_view(['GET'])
# 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
@permission_classes([IsAuthenticatedOrReadOnly])
def movie_sort(request, sort_num):
    # 장르에 따른 정렬
    genre_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    if sort_num in genre_ids:
        sort_movies = movies.filter(genres__id=sort_num).order_by('-release_date')[:30]
    elif sort_num == 20:  # 관객수(popularity)
        sort_movies = movies.order_by('-popularity')[:30]
    elif sort_num == 21:  # 최신순(개봉한 영화만)
        sort_movies = movies.filter(
            release_date__lte=date.today()).order_by('-release_date')[:30]
    elif sort_num == 22:  # 개봉예정작 : 빠른 개봉 순으로
        sort_movies = movies.filter(
            release_date__gt=date.today()).order_by('release_date')[:30]
    elif sort_num == 23:  # 평점순(vote_average/개봉한 영화)
        sort_movies = movies.filter(
            release_date__lte=date.today()).order_by('-vote_average')[:30]
    # 장르 포함
    else:
        return Response({'error': 'Invalid sort number'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(MovieSerializer(sort_movies, many=True).data)

# # (추천)역대급 영화
# def best_movie(request):
#     pass


# # (추천)날씨별 추천 영화  
# def for_weather(request):
#     pass
