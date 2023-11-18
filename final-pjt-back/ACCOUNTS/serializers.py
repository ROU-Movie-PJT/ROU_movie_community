from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from MOVIES.serializers import GenreSerializer

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
  region = serializers.CharField(max_length=50)
  birth = serializers.DateField()
  class Meta:
    model = User
    fields = ('region', 'birth',)

  def get_cleaned_data(self):
    data = super().get_cleaned_data()
    data['region'] = self.validated_data.get('region', '')
    data['birth'] = self.validated_data.get('birth', '')
    return data

# 프로필 조회 / 프로필 이미지, 지역, 생년월일 수정
class ProfileSerializer(UserDetailsSerializer):
  class UserSerializer(serializers.ModelSerializer):
    class Meta:
      model = User
      fields = ('id',)

  hate_genres = GenreSerializer(many=True, read_only=True)
  like_genres = GenreSerializer(many=True, read_only=True)
  followers = UserSerializer(many=True)

  class Meta:
    model = User
    fields = ('id', 'followers', 'username', 'profile_image', 'region', 'followings', 'hate_genres', 'like_genres', 'birth', 'rate_image')

# 사용자 불호 장르 조회/수정
class HateGenreSerializer(serializers.ModelSerializer):
  hate_genres = GenreSerializer(many=True, read_only=True)

  class Meta:
    model = User
    fields = ('id', 'username', 'hate_genres', )

# 사용자 선호 장르 조회/수정
class LikeGenreSerializer(serializers.ModelSerializer):
  like_genres = GenreSerializer(many=True, read_only=True)

  class Meta:
    model = User
    fields = ('id', 'username', 'like_genres', )