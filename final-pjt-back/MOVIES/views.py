from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MovieTitleSerializer, MovieListSerializer
from .models import Movie


# Create your views here.
@api_view(['GET'])
def index(request):
    movies = Movie.objects.all()
    serializer = MovieTitleSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieListSerializer(movie)
    return Response(serializer.data)


def recommended(request):
    pass

