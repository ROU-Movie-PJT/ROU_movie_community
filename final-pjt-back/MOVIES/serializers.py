from rest_framework import serializers
from COMMUNITY.models import Review
from .models import *
from django.contrib.auth import get_user_model


User = get_user_model()


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'
        read_only_fields = ('person_id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        read_only_fields = ('genre_id',)


class TrendSerializer(serializers.ModelSerializer):
    class GenreSerializer(serializers.ModelSerializer):

        class Meta:
            model = Genre
            # 단일 컬럼 출력 시 ,(콤마) 필수(없으면 인식 못함)
            fields = '__all__'

    class ActorSerializer(serializers.ModelSerializer):

        class Meta:
            model = Actor
            # 단일 컬럼 출력 시 ,(콤마) 필수(없으면 인식 못함)
            fields = '__all__'

    genres = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        required=False  # 변경: 필드를 선택적으로 만듭니다.
    )

    actors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Actor.objects.all(),
        required=False  # 변경: 필드를 선택적으로 만듭니다.
    )

    class Meta:
        model = Trend
        fields = '__all__'
        read_only_fields = ('movie_id', 'release_date',)

class MovieDetailSerializer(serializers.ModelSerializer):
    class GenreSerializer(serializers.ModelSerializer):

        class Meta:
            model = Genre
            # 단일 컬럼 출력 시 ,(콤마) 필수(없으면 인식 못함)
            fields = '__all__'

    class ActorSerializer(serializers.ModelSerializer):

        class Meta:
            model = Actor
            # 단일 컬럼 출력 시 ,(콤마) 필수(없으면 인식 못함)
            fields = '__all__'
    
    actors = ActorSerializer(many=True)
    genres = GenreSerializer(many=True)
    like_movie_users_count = serializers.IntegerField(source='like_movie_users.count', read_only=True)
    dislike_movie_users_count = serializers.IntegerField(source='dislike_movie_users.count', read_only=True)
    favorite_movie_users_count = serializers.IntegerField(source='favorite_movie_users.count', read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        required=False  # 변경: 필드를 선택적으로 만듭니다.
    )

    actors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Actor.objects.all(),
        required=False  # 변경: 필드를 선택적으로 만듭니다.
    )
    


    like_movie_users_count = serializers.IntegerField(
        read_only=True)  # 좋아요한 사용자 수
    dislike_movie_users_count = serializers.IntegerField(
        read_only=True)  # 영화를 싫어요한 사용자
    watching_movie_users_count = serializers.IntegerField(
        read_only=True)  # 영화를 시청한 사용자
    favorite_movie_users_count = serializers.IntegerField(
        read_only=True)  # 영화를 찜한 사용자
    # review_movie_count = serializers.IntegerField()  # 리뷰글의 수

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('movie_id', 'release_date', 'like_movie_users_count',
                            'dislike_movie_users_count', 'watching_movie_users_count', 'favorite_movie_users_count', 'review_movie_count')

# 영화별 게시글 조회
class MovieReviewSerializer(serializers.ModelSerializer):

    class ReviewSerializer(serializers.ModelSerializer):
        class UserSerializer(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ('id', 'username', 'profile_image')

        write_review_user = UserSerializer()

        class Meta:
            model = Review
            fields = '__all__'

    write_movie_review = ReviewSerializer(many=True)  # 영화에 작성된 게시글

    class Meta:
        model = Movie
        # 영화 id, 영화에 작성된 게시글
        fields = ('id', 'write_movie_review')

class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username',)

# 영화 좋아요 등록 및 해제
class MovieLikeSerializer(serializers.ModelSerializer):
    # 좋아요한 사용자
    like_movie_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        # 영화 id, 좋아요를 한 사용자 목록, 좋아요 수
        fields = ('id', 'like_movie_users', )


# 영화 싫어요 등록 및 해제
class MovieDisLikeSerializer(serializers.ModelSerializer):
    # 싫어요한 사용자
    dislike_movie_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        # 영화 id, 싫어요를 한 사용자 목록, 싫어요 수
        fields = ('id', 'dislike_movie_users', )


# 영화 시청 등록 및 해제
class MovieWatchingSerializer(serializers.ModelSerializer):
    # 영화 시청 사용자
    watching_movie_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        # 영화 id, 시청한 사용자 목록, 시청한 사용자 수
        fields = ('id', 'watching_movie_users', )


# 영화 찜 등록 및 해제
class MovieFavoriteSerializer(serializers.ModelSerializer):
    # 찜한 사용자
    favorite_movie_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        # 영화 id, 찜한 사용자 목록, 찜한 수
        fields = ('id', 'favorite_movie_users', )
