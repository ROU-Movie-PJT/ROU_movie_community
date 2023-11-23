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
from django.views.decorators.cache import cache_page
from .recommend import recommend_movies
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery
from .models import Movie, Actor, Genre
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
# 영화 검색 기능


def search_movies(query, actor_name=None, genre_name=None):
    queryset = Movie.objects.all()

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(overview__icontains=query)
        )

    if actor_name:
        queryset = queryset.filter(actors__name__icontains=actor_name)

    if genre_name:
        queryset = queryset.filter(genres__name__icontains=genre_name)

    return queryset


# Example usage
# search_results = search_movies(
#     query="Inception", actor_name="Leonardo DiCaprio", genre_name="Sci-Fi")


# @csrf_exempt
@require_http_methods(["GET", "POST"])
def search_view(request):
    # return JsonResponse({'status': 'success'})
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('q', '')
            actor_name = data.get('actor_name', '')
            genre_name = data.get('genre_name', '')
            # Your search logic...
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        query = request.GET.get('q', '')
        actor_name = request.GET.get('actor', '')
        genre_name = request.GET.get('genre', '')
    print(search_movies(query, actor_name, genre_name))
    results = search_movies(query, actor_name, genre_name)
    serializer = MovieSerializer(results, many=True)
    return JsonResponse(serializer.data, safe=False)


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


def api_test_video(request):
    movies = Movie.objects.all()
    for movie in movies:
        movie_id = movie.movie_id
        detail_params = {'language': 'ko-KR', 'api_key': TMDB_API_KEY,
                         'append_to_response': 'credits,videos'}
        try:
            response = requests.get(
                f'{TMDB_DETAIL_INFO_BASE_URL}{movie_id}', params=detail_params).json()

            # Debugging: Check the response
            # print(f"Response for movie ID {movie_id}: ", response)

            videos = response['videos']['results']

            # Debugging: Check the videos list
            # print(f"Videos for movie ID {movie_id}: ", videos)
            videos = response.get('videos', {}).get('results')
            if videos:
                movie.videos = videos[0].get('key')
            else:
                movie.videos = None
            print(movie)

            movie.runtime = response.get('runtime', None)

            crew_list = response['credits']['crew']
            director = next(
                (crew['name'] for crew in crew_list if crew['job'] == 'Director'), None)
            movie.director = director  # 속성 접근 방식 사용
            # Debug print
            print(f"Director for movie ID {movie_id}: ", director)

            movie.save()  # 업데이트된 모델 저장

        except json.JSONDecodeError as e:
            print(f"JSON Decode Error for movie ID {movie_id}: ", e)
        except Exception as e:
            print(f"An error occurred for movie ID {movie_id}: ", e)
    return JsonResponse({'message': 'Success'})

# TMDB 영화 트렌드


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def api_test_TT(request):
    # Trend.objects.all().delete()
    params = {
        'language': 'ko',
        'api_key': TMDB_API_KEY,
    }
    response = requests.get(TMDB_TRENDING_BASE_URL, params=params).json()
    movies_trend = response['results']

    for movie in movies_trend:
        trend_serializer = TrendSerializer(data=movie)
        if trend_serializer.is_valid(raise_exception=True):
            trend_serializer.save(movie_id=movie['id'])

    return JsonResponse({'message': 'Success'})


def api_test_video2(request):
    movies = Trend.objects.all()
    for movie in movies:
        movie_id = movie.movie_id
        detail_params = {'language': 'ko-KR',
                         'api_key': TMDB_API_KEY, 'append_to_response': 'videos'}
        try:
            response = requests.get(
                f'{TMDB_DETAIL_INFO_BASE_URL}{movie_id}', params=detail_params).json()
            videos = response.get('videos', {}).get('results')
            if videos:
                movie.videos = videos[0].get('key')
            else:
                movie.videos = None
            print(movie)
            movie.save()  # 업데이트된 모델 저장
        except json.JSONDecodeError:
            # Log error or take appropriate action
            pass
        except KeyError:
            # Log error or take appropriate action
            pass
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
    serializer = MovieDetailSerializer(movie)

    data = {
        'isLike': movie.like_movie_users.filter(pk=request.user.pk).exists(),
        'isFavorite': movie.favorite_movie_users.filter(pk=request.user.pk).exists(),
        'isDislike': movie.dislike_movie_users.filter(pk=request.user.pk).exists(), 
        'isWatch': movie.watching_movie_users.filter(pk=request.user.pk).exists()
    }

    data.update(serializer.data)

    return JsonResponse(data)


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
        isLike = False
    # 등록
    else:
        movie.like_movie_users.add(user)
        isLike = True

    serializer = MovieLikeSerializer(movie)

    like_movie_register = {
        'id': serializer.data.get('id'),
        'like_movie_users_count': movie.like_movie_users.count(),
        'like_movie_users': serializer.data.get('like_movie_users'),
        'isLike': isLike
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
        isDislike = False
    # 등록
    else:
        movie.dislike_movie_users.add(user)
        isDislike = True

    serializer = MovieDisLikeSerializer(movie)

    dislike_movie_register = {
        'id': serializer.data.get('id'),
        'dislike_movie_users_count': movie.dislike_movie_users.count(),
        'dislike_movie_users': serializer.data.get('dislike_movie_users'),
        'isDislike': isDislike
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
        isWatch = False
    # 등록
    else:
        movie.watching_movie_users.add(user)
        isWatch = True

    serializer = MovieWatchingSerializer(movie)

    watching_movie_register = {
        'id': serializer.data.get('id'),
        'watching_movie_users_count': movie.watching_movie_users.count(),
        'watching_movie_users': serializer.data.get('watching_movie_users'),
        'isWatch': isWatch
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
        isFavorite = False
    # 등록
    else:
        movie.favorite_movie_users.add(user)
        isFavorite = True

    serializer = MovieFavoriteSerializer(movie)

    favorite_movie_register = {
        'id': serializer.data.get('id'),
        'favorite_movie_users_count': movie.favorite_movie_users.count(),
        'favorite_movie_users': serializer.data.get('favorite_movie_users'),
        'isFavorite': isFavorite
    }
    return JsonResponse(favorite_movie_register)


# 박스오피스 인기 영화 조회
# 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def movie_trend(request):
    movies = Trend.objects.all()
    serializer = TrendSerializer(movies, many=True)
    return Response(serializer.data)


# # (추천)장르별 추천 영화 조회
@api_view(['GET'])
# 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
@permission_classes([IsAuthenticatedOrReadOnly])
def movie_genre(request, genre_id):
    genre_movie = movies.filter(
        genres=genre_id,
        release_date__lte=date.today()).order_by('-popularity')[:10]
    serializer = MovieSerializer(genre_movie, many=True)
    return Response(serializer.data)


# 필터링된 영화 정보
# @cache_page(60 * 30)  # Cache for 15 minutes
@api_view(['GET'])
# 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
@permission_classes([IsAuthenticatedOrReadOnly])
def movie_sort(request, sort_num):
    # 장르에 따른 정렬
    genre_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9,
                 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    if sort_num in genre_ids:
        sort_movies = movies.filter(
            genres__id=sort_num).order_by('-release_date')[:30]
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


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def person_detail(request, actor_id):
    person = Actor.objects.get(id=actor_id)
    serializer = ActorSerializer(person)
    return Response(serializer.data)


@api_view(['GET'])
def movie_recommendation(request, title):
    recommended_movies = recommend_movies(request.user.id, title)  # user_id 대신 request.user를 전달합니다.
    serializer = MovieRecommendSerializer(recommended_movies, many=True)
    return Response({'recommended_movies': serializer.data})