import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from .serializers import *
from MOVIES.models import Genre
from django.http import JsonResponse

User = get_user_model()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete(request):
    request.user.delete()
    return Response({'message': f'사용자 {request.user} 탈퇴 완료!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.method == 'GET':
        serializer = ProfileSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        if request.user == user:
            serializer = ProfileSerializer(
                instance=user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def preference(request, pType):
    user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'GET':
        if pType == 'like':
            serializer = LikeGenreSerializer(user)
        elif pType == 'hate':
            serializer = HateGenreSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        genres = request.data['genres'].split(',')
        if pType == 'like':
            for genre_name in genres:
                genre = get_object_or_404(Genre, name=genre_name)
                if user.like_genres.filter(id=genre.id).exists():
                    user.like_genres.remove(genre)
                else:
                    user.like_genres.add(genre)
            serializer = LikeGenreSerializer(user)
        elif pType == 'hate':
            for genre_name in genres:
                genre = get_object_or_404(Genre, name=genre_name)
                if user.hate_genres.filter(id=genre.id).exists():
                    user.hate_genres.remove(genre)
                else:
                    user.hate_genres.add(genre)
            serializer = HateGenreSerializer(user)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.user != user:
        if user.followers.filter(pk=request.user.pk).exists():
            user.followers.remove(request.user)
        else:
            user.followers.add(request.user)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)
    else:
        return Response({'detail': '본인은 팔로우 불가'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def follow_list(request, user_pk):
    follow_user = get_object_or_404(User, pk=user_pk)
    serializer = FollowSerializer(follow_user)

    follow_status = {
        # 팔로워
        'follower_count': follow_user.followings.count(),
        # 팔로워(from_user_id가 팔로우 당한사람 : user_pk)(followings가 팔로우를 한 사람) 목록
        'follow_list': serializer.data.get('followings'),
        # 팔로잉 수
        'following_count': follow_user.followers.count(),
    }
    return JsonResponse(follow_status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_friend(request, user_pk):
    me = get_object_or_404(User, pk=user_pk)
    # user = request.user # username이 출력
    serializer = ProfileSerializer(me)  # 나의 정보를 추출
    # 연도 추출 : 나의 나이 +-3
    year = int(serializer.data.get('birth')[:4])
    first_date = datetime.date(year - 3, 1, 1)
    last_date = datetime.date(year + 3, 12, 31)
    # 나를 제외하고 지역이 같은 사람을 추출
    friends = User.objects.filter(
        region=serializer.data.get('region'),
        birth__range=(first_date, last_date)).exclude(username=me)
    serializer = ProfileSerializer(friends, many=True)
    if friends.exists():
        return Response(serializer.data)
    else:
        data = {
            'content': f'추천 친구가 없습니다.',
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hate_genre_list(request, user_pk):
    Users = get_object_or_404(User, pk=user_pk)
    serializer = HateGenreSerializer(Users)
    user_hate_list = {
        'id': serializer.data.get('id'),
        'username': serializer.data.get('username'),
        'hate_genres_count': Users.hate_genres.count(),
        'hate_genres': serializer.data.get('hate_genres'),
    }
    return JsonResponse(user_hate_list)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def hate_genre_update_or_delete(request, user_pk, genre_pk):
    user_genre = get_object_or_404(User, pk=user_pk)
    genre_picks = get_object_or_404(Genre, pk=genre_pk)
    genre = genre_picks.id

    if user_genre.hate_genres.filter(pk=genre_pk).exists():
        user_genre.hate_genres.remove(genre)
    else:
        user_genre.hate_genres.add(genre)

    serializer = HateGenreSerializer(user_genre)

    user_hate_register = {
        'id': serializer.data.get('id'),
        'username': serializer.data.get('username'),
        'hate_genres_count': user_genre.hate_genres.count(),
        'hate_genres': serializer.data.get('hate_genres'),
    }

    return JsonResponse(user_hate_register)
