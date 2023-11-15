# from django.shortcuts import render, get_object_or_404
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.http import JsonResponse
# from rest_framework import status
# from .serializers import MovieTitleSerializer, MovieListSerializer
# from .models import Movie
# import requests

# BASE_URL = 'https://api.themoviedb.org/3/movie/popular'
# API_KEY = '49d792ca8a7053508d689eedb328f369'

# # 감독, 배우, 영화 다 조회 가능
# # https://api.themoviedb.org/3/movie/247?api_key=49d792ca8a7053508d689eedb328f369&language=ko-KR&append_to_response=credits
# # Create your views here.


# @api_view(['GET'])
# def api_test(request):
#     for page in range(1, 11):
#         params = {
#             'language': 'ko-KR',
#             'api_key': API_KEY,
#             'append_to_response': credits
#         }
#         response = requests.get(BASE_URL, params=params).json()
#         movie_list = response['results']

#         for movie in movie_list:
#             genres = movie['genre_ids']
#             movie['genre'] = genres
#             movieserializer = MovieListSerializer(data=movie)
#             if movieserializer.is_valid(raise_exception=True):
#                 movieserializer.save()
#     return JsonResponse({'message': 'Success'})

# @api_view(['GET'])
# def api_test(request):


# @api_view(['GET'])
# def index(request):
#     movies = Movie.objects.all()
#     serializer = MovieTitleSerializer(movies, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def detail(request, movie_pk):
#     movie = get_object_or_404(Movie, pk=movie_pk)
#     serializer = MovieListSerializer(movie)
#     return Response(serializer.data)


# def recommended(request):
#     pass
